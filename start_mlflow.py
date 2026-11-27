"""Start the MLflow UI using the same tracking store as training and the API."""
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", (root / "mlruns").as_uri())
print(f"Starting MLflow UI with tracking store: {tracking_uri}", flush=True)
raise SystemExit(subprocess.call([sys.executable, "-m", "mlflow", "ui", "--backend-store-uri", tracking_uri, *sys.argv[1:]]))
