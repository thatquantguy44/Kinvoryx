# iOS Research Testing

How to get the Capital Allocation Decision Brief onto a phone for GATE-M3 discovery interviews.

Two paths exist depending on what you need: a static shared URL for quick walkthroughs, and a local Wi-Fi server for testing with participants on their own devices.

---

## Option A — Published Artifact (quickest)

The combined brief is published as a Claude Artifact at:

```
https://claude.ai/code/artifact/835a3260-72af-47b3-8e69-6f6186bc0df3
```

Open that URL in Mobile Safari on any device. No server, no Wi-Fi dependency. The page is self-contained and works offline once loaded.

**Use this when:**
- Running a screen-share or over-the-shoulder walkthrough
- Sharing a link with a participant before the session
- Demoing the layout to a stakeholder

**Limitation:** The data is fixed to the synthetic demo household. Updating it requires regenerating and republishing the artifact from this Claude Code session.

### Republishing after changes

To regenerate with updated optimizer output:

```bash
cd /path/to/Kinvoryx
python /path/to/scratchpad/gen_artifact.py
```

Then republish by opening this conversation in Claude Code and running the Artifact publish step again. The URL stays the same.

---

## Option B — Local Wi-Fi Server

Serves the combined HTML over your local network. Any iOS device on the same Wi-Fi can open it in Mobile Safari.

### Prerequisites

- Python 3.11+ (already required by the project)
- Laptop and iOS device on the **same Wi-Fi network**

### Running

```bash
cd /path/to/Kinvoryx
python examples/demo/optimizer_decision_brief.py --serve
```

Output:

```
Open in Mobile Safari → http://192.168.1.42:8080/
Ctrl-C to stop.
```

Type that URL into Safari on the iPhone. The page loads the combined Household + Reviewer brief for the synthetic demo household.

To use a different port:

```bash
python examples/demo/optimizer_decision_brief.py --serve --port 9000
```

**Use this when:**
- Watching a participant navigate on their own phone
- Testing gesture behavior, scroll, and tap targets on a real device
- Running sessions where screen recording the device separately

### Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Safari shows "Cannot connect" | Different Wi-Fi networks | Confirm both devices show the same SSID |
| Address bar shows a different IP | Multiple network interfaces | Run `ipconfig getifaddr en0` (Mac) to find the correct one |
| Port 8080 refused | Port already in use | Add `--port 9000` |
| Page doesn't load after Ctrl-C | Server stopped | Re-run the command |

---

## What the page contains

Both options serve the same two-tab page:

**Household tab** — what a research participant sees first:
- Three key numbers: annual income, fixed obligations, annual surplus
- Comparison table across four allocation alternatives (Waterfall Baseline, Recommended, Liquidity-Preserving, Goal Acceleration)
- Allocation detail for the Recommended alternative
- Four deterministic stress scenarios (income loss, unexpected expense, market decline, goal cost increase)
- Common assumptions

**Reviewer tab** — internal audit layer:
- Household fingerprint (SHA-256)
- Income sources with provenance and freshness
- Debt table (balance, APR, monthly minimum)
- Full detail and scenario tables for all four alternatives
- Binding constraints and opportunity costs per alternative

The disclosure banner appears in both tabs: *Synthetic decision-support prototype only.*

---

## Research session notes

- The Household tab is the right starting point for participants. Ask them to read it aloud and narrate what they'd do next.
- The comparison table is the highest-signal moment — watch whether participants understand the four alternatives without prompting.
- The Reviewer tab is for internal review only; do not show it to participants unless they ask to see more detail.
- The synthetic household ($335K gross, dual income, RSU comp, student loans, home down payment goal) is chosen to match the GATE-M3 target profile. Adjust the demo household in `examples/demo/optimizer_decision_brief.py` if testing a different profile.

---

## Updating the demo household

The synthetic household is defined in `_demo_household()` in `examples/demo/optimizer_decision_brief.py`. Edit income sources, debts, or goals there, then re-run with `--serve` or `--save` to see the updated output.

To save all five artifacts (Markdown + HTML) to `examples/demo/out/`:

```bash
python examples/demo/optimizer_decision_brief.py --save
```

---

## Related

- `src/kinvoryx/optimizer_rendering.py` — rendering layer for all HTML and Markdown output
- `src/kinvoryx/capital_allocation_optimizer.py` — Spec 004 optimizer
- `examples/demo/optimizer_decision_brief.py` — demo entry point
- `docs/specs/004-capital-allocation-optimizer.md` — optimizer specification
- `docs/specs/007-validation-and-market-research.md` — GATE-M3 criteria
