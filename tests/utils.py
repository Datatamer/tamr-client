import json
from pathlib import Path

data_dir = Path(__file__).parent / "data"


def load_json(path: Path):
    with open(path) as f:
        return json.load(f)
