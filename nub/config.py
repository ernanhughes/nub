import os
import os.path
from pathlib import Path
from tempfile import gettempdir
from typing import Any

from click import UsageError
from dotenv import load_dotenv

from nub.utils import get_default_data_dir

load_dotenv()

CONFIG_FOLDER = os.path.expanduser("~/.config")
SUMMARIZER_CONFIG_FOLDER = Path(CONFIG_FOLDER) / "nub"
TEMP_DATA_PATH = Path(gettempdir()) / "data"
CACHE_PATH = Path(gettempdir()) / "cache"

DEFAULT_CONFIG = {
    "ENV": "development",
    "OLLAMA_HOST": "localhost:11434",
    "BASEDIR": os.path.abspath(os.path.dirname(__file__)),
    "USE_DATABASE": "false",
    "SCHEMA_FILE": "schema.sql",
    "DATABASE_PATH": os.environ.get("DATABASE_PATH", "nub.db"),
    "DATABASE_URL": os.environ.get("DATABASE_URL", "sqlite:///nub.db"),
    "OLLAMA_URL": os.environ.get("OLLAMA_URL", "http://127.0.0.1:5000"),
    "OLLAMA_MODEL": os.environ.get("OLLAMA_MODEL", "llama3.1"),
    "DATA_DIR": Path(get_default_data_dir("nub")),
    "LOG_FILE": str(os.environ.get("LOG_FILENAME", "nub.log")),
}


class Config(dict):
    def __init__(self, config_path: Path, **defaults: Any):
        self.config_path = config_path
        print(f"Config path: {config_path}")
        if self._exists():
            self._read()
            has_new_config = False
            for key, value in defaults.items():
                if key not in self:
                    has_new_config = True
                    self[key] = value
                    print("Key: {key} Value:{value}")
            if has_new_config:
                self._write()
        else:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            super().__init__(**defaults)
            self._write()

    def _exists(self) -> bool:
        return os.path.isfile(self.config_path)

    def _write(self) -> None:
        with open(self.config_path, "w", encoding="utf-8") as file:
            string_config = ""
            for key, value in self.items():
                string_config += f"{key}={value}\n"
            file.write(string_config)

    def _read(self) -> None:
        with open(self.config_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    self[key] = value

    def get(self, key: str) -> str:  # type: ignore
        # Prioritize environment variables over config file.
        value = super().get(key) or os.getenv(key)
        if not value:
            raise UsageError(f"Missing config key: {key}")
        return value


appConfig = Config(SUMMARIZER_CONFIG_FOLDER, **DEFAULT_CONFIG)
