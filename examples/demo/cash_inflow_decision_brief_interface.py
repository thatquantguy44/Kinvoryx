"""Run the local manual-entry interface for the synthetic Spec 011 brief."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from kinvoryx.cash_inflow_interface import serve_manual_entry


def main() -> None:
    host = "127.0.0.1"
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    server = serve_manual_entry(host, port)
    print(f"Serving synthetic cash-inflow interface at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
