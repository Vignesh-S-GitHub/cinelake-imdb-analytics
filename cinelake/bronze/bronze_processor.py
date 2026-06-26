from datetime import datetime
from pathlib import Path

import polars as pl
from deltalake import write_deltalake
from loguru import logger

from cinelake.config.settings import Settings


class BronzeProcessor:
    """Processes raw IMDb datasets into Bronze Delta tables."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        self.raw_dir = Path("data") / settings.raw_prefix
        self.bronze_dir = Path("data") / settings.bronze_prefix

        self.bronze_dir.mkdir(parents=True, exist_ok=True)

    def process_all(self) -> None:
        """Process all configured IMDb datasets."""

        logger.info("Starting Bronze layer processing...")

        for dataset_name, file_name in self.settings.datasets.items():
            try:
                self.process_dataset(dataset_name, file_name)
            except Exception as exc:
                logger.exception(
                    f"Failed processing dataset '{dataset_name}': {exc}"
                )

        logger.success("Bronze layer completed.")

    def process_dataset(self, dataset_name: str, file_name: str) -> None:
        """Process a single IMDb dataset."""

        logger.info(f"Processing dataset: {dataset_name}")

        raw_file = self.raw_dir / file_name

        df = self._read_dataset(raw_file)
        self._validate_dataset(df, raw_file)
        df = self._add_metadata(df, file_name)
        self._write_delta(df, dataset_name)

        logger.success(f"{dataset_name} processed successfully.")

    def _read_dataset(self, file_path: Path) -> pl.DataFrame:
        """Read a compressed IMDb TSV file."""

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        logger.info(f"Reading {file_path.name}")

        return pl.read_csv(
                file_path,
                separator="\t",
                null_values="\\N",
                infer_schema_length=0,
                quote_char=None
                )

    def _validate_dataset(
        self,
        df: pl.DataFrame,
        file_path: Path,
    ) -> None:
        """Perform basic dataset validation."""

        if df.is_empty():
            raise ValueError(f"{file_path.name} is empty.")

        logger.info(
            f"{file_path.name}: "
            f"{df.height:,} rows, {df.width} columns"
        )

    def _add_metadata(
        self,
        df: pl.DataFrame,
        file_name: str,
    ) -> pl.DataFrame:
        """Add Bronze metadata columns."""

        ingestion_time = datetime.utcnow()

        return df.with_columns(
            [
                pl.lit(ingestion_time).alias("_ingestion_time"),
                pl.lit(file_name).alias("_source_file"),
            ]
        )

    def _write_delta(
        self,
        df: pl.DataFrame,
        dataset_name: str,
    ) -> None:
        """Write DataFrame to Delta Lake."""

        output_path = self.bronze_dir / dataset_name

        logger.info(f"Writing Delta table -> {output_path}")

        write_deltalake(
            str(output_path),
            df.to_arrow(),
            mode="overwrite",
        )