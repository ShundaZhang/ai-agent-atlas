# AI & Agent Atlas

An independent bilingual learning site about AI, LLMs, agents and harness engineering, with ChatGPT and Codex as practical examples.

Live site: https://shundazhang.github.io/ai-agent-atlas/

- 18 chapter pages in English and Chinese (36 HTML files)
- 14 original semantic HTML diagrams per language
- 40 searchable glossary terms
- 39 primary papers, author-maintained textbooks and official guides
- 3 deterministic browser exercises, a downloadable Python teaching runtime and a bilingual task notebook

English is the default. The EN / 中文 control uses the same language preference as the other ShundaZhang learning sites. The site is static and needs no model account or API key.

## Contents

Concepts; LLM mechanics; training; inference; prompting; context and RAG; agents; harness; tools and MCP; Codex; ChatGPT; evaluation; security; practice; labs; glossary; sources.

The material separates stable theory from changing product interfaces. Product guidance was reviewed on 30 September 2026. Research experiments are labeled by their historical dates and are not described as current commercial model internals. External resources are linked, not mirrored.

## Build and preview

```sh
python3 -B build.py
python3 -m http.server 8769 --bind 127.0.0.1
```

Open http://localhost:8769/ in a browser. No build dependencies beyond Python's standard library are required. GitHub Pages serves the committed static files from `main` at `/`.

Edit `content.py` for chapter notes and citations, `diagrams.py` for figures, `glossary.py` for terms and `build.py` for the shell, overview and exercise markup. Rebuild instead of directly editing generated HTML.

## Exercise contracts

`labs.js` uses only in-memory synthetic data and updates local DOM output. It makes no model/tool/network calls and persists no exercise input. Only the shared language preference is saved by `language.js`.

- Context budget: invented accounting units demonstrate capacity versus exact evidence. They do not represent a tokenizer, attention model or price estimate.
- Harness trace: fixed proposals demonstrate schema/policy/execution/observation/verification and bounded stops. They do not evaluate a real model's reasoning or injection resistance.
- Evaluation: three fictional candidates and six fixed tasks demonstrate accepted-result denominators, policy violations and cost units. They do not rank real products or estimate uncertainty.

`labs/toy_harness.py` is a task-specific teaching runtime with a scripted planner and in-memory invoices. It performs no network access, explicit file writes or subprocess execution. The timeout is injected, not a real timer. It is not an SDK, production sandbox or general security library.

Save the two downloadable Python files together, then run:

```sh
python3 -B toy_harness.py success --max-steps 4
python3 -B toy_harness.py denied
python3 -B -m unittest -v test_toy_harness.py
```

The checks cover actual completion evidence, denial before execution, unsupported/wrong finals, timeout, step bounds, malformed proposals and data-grounded computation.
