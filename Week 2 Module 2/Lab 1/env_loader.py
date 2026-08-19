import os
from pathlib import Path


def load_env_file(env_path=None):
    if os.environ.get("ANTHROPIC_API_KEY"):
        return
    if env_path is None:
        env_path = Path(__file__).resolve().parent.parent / ".env"
    env_path = Path(env_path)
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if value.startswith("{") and value.endswith("}"):
            value = value[1:-1].strip()
        value = value.strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


load_env_file()
