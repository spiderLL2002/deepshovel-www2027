#!/usr/bin/env python3
"""Reproduce the paper's retrieval, argument, and research results in one environment."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import venv

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True, help='New output directory')
    parser.add_argument('--live', action='store_true', help='Also execute the frozen A/B queries')
    parser.add_argument('--base-url', help='Service URL for --live')
    parser.add_argument('--limit-per-group', type=int, help='Online queries per group (default: all queries)')
    args = parser.parse_args()
    if sys.version_info[:2] != (3, 12):
        parser.error('Run with Python 3.12')
    if args.live and not args.base_url:
        parser.error('--live requires --base-url')
    if args.limit_per_group is not None and args.limit_per_group < 1:
        parser.error('Online query limit must be positive')
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    environment = output / 'environment'
    report = {'passed': False, 'live': args.live, 'steps': []}
    env = os.environ.copy()
    env.update(PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1', DEEPSHOVEL_REPO=str(ROOT))
    env.pop('PYTHONPATH', None)
    def run(name, command):
        start = time.monotonic()
        with (output / f'{name}.log').open('w') as log:
            proc = subprocess.run([str(x) for x in command], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
        report['steps'].append({'name': name, 'exit_code': proc.returncode, 'seconds': time.monotonic()-start})
        print(('PASS ' if proc.returncode == 0 else 'FAIL ') + name, flush=True)
        if proc.returncode:
            raise RuntimeError(f'{name}: see {output / (name + ".log")}')
    try:
        run('release-files', [sys.executable, ROOT / 'scripts/verify-release.py'])
        venv.EnvBuilder(with_pip=True).create(environment)
        python = environment / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
        run('dependencies', [python, '-m', 'pip', 'install', '-r', ROOT / 'repro/requirements-paper.lock'])
        run('evaluation-metrics', [python, ROOT / 'artifact/benchmark/recompute.py'])
        run('argument-expansion', ['node', '--experimental-strip-types', '--no-warnings', ROOT / 'artifact/arguments/verify.mjs', '--out', output / 'arguments'])
        run('research-sources', [python, ROOT / 'artifact/gp15/fetch_external_sources.py'])
        run('research-claims', [python, ROOT / 'artifact/gp15/verify_demo.py'])
        run('research-trace', [python, ROOT / 'artifact/research-trace/verify_trace.py'])
        run('research-computation', [python, ROOT / 'artifact/gp15/run_portable.py', '--out', output / 'gp15'])
        if args.live:
            command = [python, ROOT / 'artifact/benchmark/run_online.py', '--out', output / 'online',
                       '--base-url', args.base_url]
            if args.limit_per_group is not None:
                command += ['--limit-per-group', args.limit_per_group]
            run('online-evaluation', command)
        report['passed'] = True
    finally:
        (output / 'report.json').write_text(json.dumps(report, indent=2)+'\n')
        print('Report: ' + str(output / 'report.json'), flush=True)


if __name__ == '__main__':
    main()
