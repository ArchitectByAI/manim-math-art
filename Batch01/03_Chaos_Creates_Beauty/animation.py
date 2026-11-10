"""Chaos Creates Beauty — Using Python. Entry point for the shared batch renderer."""
from pathlib import Path
import subprocess, sys
renderer = Path(__file__).resolve().parent.parent / "render_batch.py"
if not renderer.is_file():
    raise SystemExit("Missing shared render_batch.py in the Batch01 parent folder.")
raise SystemExit(subprocess.call([sys.executable, str(renderer), "--episode", "3"]))
