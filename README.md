# Kinvoryx

Spec-driven prototype for Household Decision Intelligence, beginning with the Household Capital Allocation Optimizer.

The first vertical slice is the synthetic-only Cash Inflow Allocation Decision Brief in [Spec 011](docs/specs/011-cash-inflow-allocation-decision-brief.md). It compares seven transparent allocation alternatives for a discrete inflow; it does not execute actions or provide personalized financial advice.

Run the synthetic demonstration with:

```sh
python3 examples/demo/cash_inflow_decision_brief.py
```

Run the deterministic validation harness and unit tests with:

```sh
python3 -m unittest discover -s tests -v
```

Preview the household and reviewer export artifacts with:

```sh
python3 examples/demo/cash_inflow_decision_brief_export.py
```

Run the local synthetic manual-entry interface with:

```sh
python3 examples/demo/cash_inflow_decision_brief_interface.py
```

## Capital Allocation Optimizer

The second vertical slice is the Household Capital Allocation Optimizer in [Spec 004](docs/specs/004-capital-allocation-optimizer.md). Given a household's income, debts, and goals it produces four allocation alternatives (waterfall baseline, recommended, liquidity-preserving, goal-acceleration), four deterministic stress scenarios per alternative, and binding constraint and opportunity cost analysis.

Run the synthetic demo and print Markdown output:

```sh
python3 examples/demo/optimizer_decision_brief.py
```

Save all five artifacts (Markdown + HTML) to `examples/demo/out/`:

```sh
python3 examples/demo/optimizer_decision_brief.py --save
```

Serve the combined HTML over local Wi-Fi for iOS testing:

```sh
python3 examples/demo/optimizer_decision_brief.py --serve
# Open in Mobile Safari → http://<printed-ip>:8080/
```

Run the interactive form server — lets participants enter their own household data in a browser and receive a live brief:

```sh
python3 examples/demo/optimizer_form_server.py
# Local:    http://localhost:8080/
# On phone: http://<printed-ip>:8080/  (same Wi-Fi)
```

Both servers accept `--port <n>` to change the default port of 8080. See [docs/deployment/ios-research-testing.md](docs/deployment/ios-research-testing.md) for research session guidance.
