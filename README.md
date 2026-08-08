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
