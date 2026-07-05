#!/usr/bin/env python3
"""aeo-audit-lite — does AI recommend your product? A tiny self-check.

Runs a buyer prompt against an AI engine several times and measures how often
your brand is mentioned versus named competitors — your "share of model" — with
a Wilson confidence interval (because a single AI answer is noise).

- Stdlib only. No pip install.
- MOCK mode by default (illustrative numbers, runs offline).
- Real mode: set PERPLEXITY_API_KEY or OPENAI_API_KEY and pass --engine.

This is the free, lite cousin of the engine we run at Clear Cited. The real
service measures more prompts across more engines, with human QC.

Examples
--------
    python aeo_audit_lite.py --brand "Acme" --competitors "Datadog,Grafana" \\
        --prompt "best observability tool for a Series A startup" --runs 10

    PERPLEXITY_API_KEY=... python aeo_audit_lite.py --brand "Acme" \\
        --competitors "Datadog,Grafana" --prompt "best APM" --runs 10 --engine perplexity

Made by Clear Cited — https://clearcited.com
"""
from __future__ import annotations
import argparse, json, math, os, random, re, sys, urllib.request, urllib.error


def wilson(k, n, z=1.96):
    """95% Wilson score interval for k successes in n trials -> (low, high) in %."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return (round(100 * max(0, centre - half), 1), round(100 * min(1, centre + half), 1))


def mentions(text, name):
    return re.search(r"\b" + re.escape(name.lower()) + r"\b", text.lower()) is not None


def ask_perplexity(prompt, key):
    body = json.dumps({"model": "sonar", "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request("https://api.perplexity.ai/chat/completions", data=body,
                                 headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["choices"][0]["message"]["content"]


def ask_openai(prompt, key):
    body = json.dumps({"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=body,
                                 headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["choices"][0]["message"]["content"]


def mock_answer(prompt, brand, competitors, seed):
    """Deterministic pseudo-answer so the tool runs offline. Illustrative only."""
    rng = random.Random(hash((prompt, seed)) & 0xffffffff)
    named = []
    # competitors tend to appear more often than a less-visible brand (the gap)
    for c in competitors:
        if rng.random() < 0.65:
            named.append(c)
    if rng.random() < 0.30:
        named.append(brand)
    rng.shuffle(named)
    return "Some good options are: " + ", ".join(named) + "." if named else "It depends on your needs."


def run(brand, competitors, prompt, runs, engine, key, mock):
    names = [brand] + competitors
    counts = {n: 0 for n in names}
    for i in range(runs):
        if mock:
            text = mock_answer(prompt, brand, competitors, i)
        elif engine == "perplexity":
            text = ask_perplexity(prompt, key)
        else:
            text = ask_openai(prompt, key)
        for n in names:
            if mentions(text, n):
                counts[n] += 1
    return counts


def main():
    ap = argparse.ArgumentParser(description="Measure your AI share-of-model for a buyer prompt.")
    ap.add_argument("--brand", required=True)
    ap.add_argument("--competitors", default="", help="comma-separated")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--runs", type=int, default=10)
    ap.add_argument("--engine", choices=["perplexity", "openai"], default="perplexity")
    ap.add_argument("--mock", action="store_true", help="force offline mock mode")
    a = ap.parse_args()

    competitors = [c.strip() for c in a.competitors.split(",") if c.strip()]
    key = os.environ.get("PERPLEXITY_API_KEY" if a.engine == "perplexity" else "OPENAI_API_KEY", "")
    mock = a.mock or not key
    mode = "MOCK (illustrative — set an API key for real data)" if mock else ("LIVE via " + a.engine)

    print('Prompt: "%s"' % a.prompt)
    print("Runs: %d   Mode: %s\n" % (a.runs, mode))
    try:
        counts = run(a.brand, competitors, a.prompt, a.runs, a.engine, key, mock)
    except urllib.error.HTTPError as e:
        sys.exit("API error %s: %s" % (e.code, e.read().decode()[:200]))

    total = sum(counts.values()) or 1
    rows = sorted(counts.items(), key=lambda kv: -kv[1])
    print("%-24s %7s  %-16s %s" % ("brand", "rate", "95% CI", "share"))
    print("-" * 60)
    for name, k in rows:
        low, high = wilson(k, a.runs)
        share = 100 * k / total
        tag = "  <- you" if name == a.brand else ""
        print("%-24s %4d/%-2d  [%4.1f–%4.1f%%]   %4.1f%%%s" % (name, k, a.runs, low, high, share, tag))
    you = counts[a.brand]
    print("\nYour share of model: %.1f%% (mentioned in %d of %d answers)." % (100 * you / total, you, a.runs))
    if mock:
        print("These are mock numbers. Run a real audit: https://clearcited.com/free-teardown/")


if __name__ == "__main__":
    main()
