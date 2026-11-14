"""Two-stage online runner checks using synthetic HTTP replies."""
from contextlib import contextmanager, redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('online_runner', ROOT / 'artifact/benchmark/run_online.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


@contextmanager
def service(tasks, fail=False):
    by_query = {task['case']['query']: task['case'] for task in tasks}
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_POST(self):
            payload = json.loads(self.rfile.read(int(self.headers['content-length'])))
            requests.append(payload)
            case = by_query[payload['query']]
            target = {'snapshotId': case['snapshot_id'], 'claim': {'id': case['claim_id']}}
            other = {'snapshotId': 'snapshot:other', 'claim': {'id': 'claim:other'}}
            streamed = payload['stage'] == 'preview'
            if fail:
                body = {'ok': False, 'error': {'code': 'INVALID_PLAN', 'message': 'Synthetic planner failure'}}
                status = 502
            elif streamed:
                body = {'ok': True, 'stage': 'preview', 'resultStatus': 'matches',
                        'queryPlanHandoff': 'sealed-test-handoff', 'previewResults': [other, target]}
                status = 200
            else:
                assert payload['query_plan_handoff'] == 'sealed-test-handoff'
                assert payload['candidate_refs'] == [
                    {'snapshot_id': 'snapshot:other', 'claim_id': 'claim:other'},
                    {'snapshot_id': case['snapshot_id'], 'claim_id': case['claim_id']}]
                target['queryRelation'] = {'relation': case['accepted_relations'][0], 'direction': case['direction']}
                body = {'ok': True, 'stage': 'ai_rerank', 'resultStatus': 'matches',
                        'clusters': [{'representative': target, 'members': [target]}]}
                status = 200
            if streamed:
                events = [{'type': 'started'}, {'type': 'heartbeat'},
                          {'type': 'result', 'status': status, 'body': body}]
                data = ''.join(json.dumps(event) + '\n' for event in events).encode()
            else:
                data = json.dumps(body).encode()
            self.send_response(200)
            self.send_header('content-type', 'application/x-ndjson' if streamed else 'application/json')
            self.send_header('content-length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}', requests
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


class OnlineEvaluationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        frozen = runner.read_json(runner.ROOT / 'online/tasks.frozen.json.gz')['tasks']
        cls.tasks = runner.select_tasks(frozen, 1, 1)
        assert len(runner.select_tasks(frozen, 100, 3)) == 600

    def execute(self, fail):
        with tempfile.TemporaryDirectory() as temporary, service(self.tasks, fail) as (url, requests):
            output = Path(temporary) / 'online'
            with redirect_stdout(io.StringIO()):
                code = runner.main(['--out', str(output), '--base-url', url,
                                    '--limit-per-group', '1', '--repetitions', '1'])
            summary = json.loads((output / 'summary.json').read_text())
            records = [json.loads(line) for line in (output / 'records.jsonl').read_text().splitlines()]
            self.assertEqual(len(records), 2)
            for record in records:
                self.assertIn('finished_at', record)
                for stage in record['stages']:
                    self.assertTrue((output / stage['request_file']).is_file())
                    self.assertTrue((output / stage['response_file']).is_file())
            for request in requests:
                self.assertNotIn('accepted_relations', request)
            return code, summary, records, requests

    def test_handoff_and_candidate_order(self):
        code, summary, _, requests = self.execute(False)
        self.assertEqual(code, 0)
        self.assertEqual(len(requests), 4)
        for group in ('A', 'B'):
            self.assertEqual(summary[group]['completed'], 1)
            self.assertEqual(summary[group]['accuracy_all_attempts'], 1)

    def test_streamed_failure_is_saved_without_retry(self):
        code, summary, records, requests = self.execute(True)
        self.assertEqual(code, 1)
        self.assertEqual(len(requests), 2)
        for record in records:
            self.assertEqual(record['stages'][0]['http_status'], 200)
            self.assertEqual(record['stages'][0]['status_code'], 502)
        for group in ('A', 'B'):
            self.assertEqual(summary[group]['failed_or_missing'], 1)
            self.assertEqual(summary[group]['accuracy_all_attempts'], 0)
            self.assertIsNone(summary[group]['mean_completed_seconds'])


if __name__ == '__main__':
    unittest.main()
