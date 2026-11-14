# DeepShovel 2.0 · WWW 2027 demonstration

DeepShovel links scientific conclusions to the observations, assumptions, reasoning steps, and original evidence needed to evaluate them.

[Demo paper](paper/main.pdf) · [English walkthrough](artifact/live-demo/README.md) · [Evaluation data](artifact/benchmark/README.md) · [Download](https://github.com/spiderLL2002/deepshovel-www2027/releases/tag/www2027-artifact)

## Reproduce the evaluation and GP15 research

Download the [evaluation package](https://github.com/spiderLL2002/deepshovel-www2027/releases/download/www2027-artifact/deepshovel-evaluation.zip) or clone this repository. From the clone, use Python 3.9 or later to recompute the [published scores](artifact/benchmark/results.json):

```sh
git clone https://github.com/spiderLL2002/deepshovel-www2027.git
cd deepshovel-www2027
python3 artifact/benchmark/recompute.py
```

To verify the release, recompute the evaluation, check the argument expander, and run the ten-stage GP15 analysis, use Python 3.12 and Node.js 22.13 or later:

```sh
python3.12 scripts/reproduce_paper.py --out runs/paper
```

To issue fresh queries, set `DEEPSHOVEL_BASE_URL` to the URL of your own configured instance:

```sh
python3 artifact/benchmark/run_online.py --base-url "$DEEPSHOVEL_BASE_URL" --out runs/online-new
```

For a small run, add `--limit-per-group 1`. See the [evaluation guide](artifact/benchmark/README.md) for inputs and outputs.

## Inspect the evidence

- [Retrieval and argument comparison](artifact/benchmark/README.md): queries, reference labels, model responses, and source audit.
- [F2 argument inspection](artifact/arguments/README.md): recorded premises, assumptions, source links, and dependency expansion.
- [GP15 study](artifact/gp15/README.md): public measurements, analysis protocol, and scripts behind the error contrasts.
- [Research trace](artifact/research-trace/README.md): queries, evidence, and research decisions.

## Run the application locally

```sh
npm run install:ci
python3 scripts/setup-local-config.py
python3.12 -m venv compiler/.venv
compiler/.venv/bin/python -m pip install -e './compiler[test]'
```

Follow the [self-hosting guide](docs/SELF_HOSTING.md) to configure your services. Start `npm run dev:compiler` and `npm run dev` in separate terminals and open the address printed by the Web process. Use the [English walkthrough](artifact/live-demo/README.md) with that instance or follow the included screenshots and source pages.

## License and citation

Project code and author-created materials are **AGPL-3.0-only**. Scientific publications, datasets, software, and vendored components retain their licenses. See [LICENSE](LICENSE), [NOTICE](NOTICE), [third-party notices](THIRD_PARTY_NOTICES.md), and [CITATION.cff](CITATION.cff).
