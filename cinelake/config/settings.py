from dataclasses import dataclass
import tomllib


@dataclass
class Settings:
    # IMDb
    base_url: str

    # Download
    timeout_seconds: int
    max_retries: int
    chunk_size: int

    # Datasets
    datasets: dict[str, str]

    # Storage
    raw_prefix: str
    bronze_prefix: str
    silver_prefix: str
    gold_prefix: str


def load_settings(config_path: str = "config/settings.toml") -> Settings:
    with open(config_path, "rb") as file:
        config = tomllib.load(file)

    return Settings(
        base_url=config["base_url"],

        timeout_seconds=config["download"]["timeout_seconds"],
        max_retries=config["download"]["max_retries"],
        chunk_size=config["download"]["chunk_size"],

        datasets=config["datasets"],

        raw_prefix=config["storage"]["raw_prefix"],
        bronze_prefix=config["storage"]["bronze_prefix"],
        silver_prefix=config["storage"]["silver_prefix"],
        gold_prefix=config["storage"]["gold_prefix"],
    )