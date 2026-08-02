# aeo-audit-lite

[![PyPI](https://img.shields.io/pypi/v/aeo-audit-lite.svg)](https://pypi.org/project/aeo-audit-lite/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21757553.svg)](https://doi.org/10.5281/zenodo.21757553)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Does AI actually recommend your product?** Run a buyer prompt against an AI
engine several times and measure how often your brand shows up versus named
competitors — your *share of model* — with a confidence interval.

A single ChatGPT screenshot proves nothing: AI answers are non-deterministic.
This measures properly, the same way every time.

- **Zero dependencies** — Python standard library only.
- **Mock mode by default** — runs offline with illustrative numbers.
- **Bring your own key** — set `PERPLEXITY_API_KEY` or `OPENAI_API_KEY` for real data.

## Install

```bash
pip install aeo-audit-lite
```

That installs an `aeo-audit-lite` command. Everything below works the same either
way — `aeo-audit-lite --mock` and `python aeo_audit_lite.py --mock` are the same
program. Python 3.9+, no dependencies.

## Usage

Offline demo (no key needed):

```bash
python aeo_audit_lite.py --brand "Acme" --competitors "Datadog,Grafana,New Relic" \
  --prompt "best observability tool for a Series A startup" --runs 12 --mock
```

Real measurement:

```bash
export PERPLEXITY_API_KEY=pplx-...
python aeo_audit_lite.py --brand "Acme" --competitors "Datadog,Grafana" \
  --prompt "best APM for kubernetes" --runs 10 --engine perplexity
```

### Example output

```
brand                       rate  95% CI           share
------------------------------------------------------------
Datadog                    10/12  [55.2–95.3%]   31.2%
Grafana                    10/12  [55.2–95.3%]   31.2%
New Relic                   8/12  [39.1–86.2%]   25.0%
Acme                        4/12  [13.8–60.9%]   12.5%  <- you

Your share of model: 12.5% (mentioned in 4 of 12 answers).
```

## How it works

1. Sends your prompt to the engine `--runs` times.
2. Checks each answer for whole-word mentions of your brand and each competitor.
3. Reports mention rate, a 95% **Wilson** confidence interval, and share of model
   (your mentions ÷ all brand mentions).

### Why repeat the prompt?

LLMs sample their output — ask twice, get two answers. One run is a coin flip.
Repeating and reporting the median/interval is the difference between data and
vibes.

## Options

| Flag | Meaning |
|---|---|
| `--brand` | your product name (required) |
| `--competitors` | comma-separated competitor names |
| `--prompt` | the buyer question (required) |
| `--runs` | number of repetitions (default 10) |
| `--engine` | `perplexity` (default) or `openai` |
| `--mock` | force offline mock mode |

## Related tools

Part of a set of five, all MIT-licensed and each archived on Zenodo with a DOI.
Find what is missing, fix it, then measure whether it moved.

| Tool | What it does |
|---|---|
| **aeo-audit-lite** | measure your share of model against competitors, with a confidence interval — *you are here* |
| [`citation-ready`](https://github.com/Clear-Cited/citation-ready) | check whether a page carries the signals cited pages tend to carry |
| [`schema-for-ai`](https://github.com/Clear-Cited/schema-for-ai) | JSON-LD templates tuned for AI extraction, plus a validator |
| [`schema-generator`](https://github.com/Clear-Cited/schema-generator) | build Organization / Product / FAQPage JSON-LD in your browser |
| [`llms-txt-generator`](https://github.com/Clear-Cited/llms-txt-generator) | generate an llms.txt for your site, in your browser |

## Cite this

Every release is archived on Zenodo with a DOI, and the repo carries a
`CITATION.cff` so GitHub’s **Cite this repository** box works.

| | DOI |
|---|---|
| **Cite the software** (always resolves to the latest version) | [10.5281/zenodo.21757553](https://doi.org/10.5281/zenodo.21757553) |
| **Cite this exact release** (v0.1.0) | [10.5281/zenodo.21757554](https://doi.org/10.5281/zenodo.21757554) |

The method behind it is written up in the protocol paper,
[10.5281/zenodo.21614890](https://doi.org/10.5281/zenodo.21614890).

## Mirror

Mirrored to Codeberg at <https://codeberg.org/clear-cited/aeo-audit-lite>, tags
included, so the project does not depend on any single host.

## License

MIT © Clear Cited

---

This is the lite version. The full **[Clear Cited](https://clearcited.com)**
service measures dozens of prompts across every major engine (ChatGPT, Perplexity,
Claude, Gemini, Google AI Overviews), with human QC and a fix roadmap.
[Get a free teardown →](https://clearcited.com/free-teardown/)
