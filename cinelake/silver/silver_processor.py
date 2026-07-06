from pathlib import Path

import polars as pl
from loguru import logger

from cinelake.config.settings import Settings
from cinelake.silver.schemas import IMDB_SCHEMAS


class SilverProcessor:
    """Processes Bronze Delta tables into Silver Delta tables."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        self.bronze_dir = Path("data") / settings.bronze_prefix
        self.silver_dir = Path("data") / settings.silver_prefix

        self.silver_dir.mkdir(parents=True, exist_ok=True)

    def process_all(self) -> None:
        for dataset_name in self.settings.datasets.keys():
            self.process_dataset(dataset_name)

    def process_dataset(self, dataset_name: str) -> None:
        logger.info(f"Reading Bronze table: {dataset_name}")

        df = self._read_bronze(dataset_name)

        self._validate_schema(dataset_name, df)

        df = self._convert_types(dataset_name, df)

        df = self._clean_strings(df)

        self._validate_primary_key(dataset_name, df)

        logger.info(f"Rows: {df.height:,}")
        logger.info(f"Columns: {df.width}")

        logger.success(f"{dataset_name} loaded successfully.")

    def _read_bronze(self, dataset_name: str) -> pl.DataFrame:
        table_path = self.bronze_dir / dataset_name

        return pl.read_delta(table_path)
    
    def _validate_schema(self, dataset_name: str, df) -> None:
        """
        Validate the Bronze table against the expected schema.
        """

        schema = IMDB_SCHEMAS.get(dataset_name)

        if schema is None:
            raise ValueError(f"No schema configuration found for '{dataset_name}'.")

        expected_columns = schema["columns"]

        # Empty table check
        if df.is_empty():
            raise ValueError(f"{dataset_name} is empty.")

        # Duplicate column check
        if len(df.columns) != len(set(df.columns)):
            raise ValueError(f"{dataset_name} contains duplicate columns.")

        # Missing columns
        missing_columns = [
            column
            for column in expected_columns
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"{dataset_name} is missing columns: {missing_columns}"
            )

        # Extra columns (optional warning)
        extra_columns = [
            column
            for column in df.columns
            if column not in expected_columns
        ]

        if extra_columns:
            logger.warning(
                f"{dataset_name} contains unexpected columns: {extra_columns}"
            )

        logger.success(f"{dataset_name} schema validation passed.")   
        
    def _convert_types(
        self,
        dataset_name: str,
        df: pl.DataFrame,
    ) -> pl.DataFrame:
        """Convert columns to configured data types."""

        schema = IMDB_SCHEMAS[dataset_name]
        type_mapping = schema["types"]

        expressions = []

        for column, dtype in type_mapping.items():

            if dtype == pl.Boolean:

                expressions.append(
                    (
                        pl.when(pl.col(column) == "1")
                        .then(True)
                        .otherwise(False)
                        .alias(column)
                    )
                )

            else:

                expressions.append(
                    pl.col(column)
                    .cast(dtype, strict=False)
                    .alias(column)
                )

        df = df.with_columns(expressions)

        logger.info(f"{dataset_name}: data types converted.")

        return df
    def _clean_strings(
        self,
        df: pl.DataFrame,
    ) -> pl.DataFrame:
        """
        Clean all string columns.
        """

        expressions = []

        for column, dtype in df.schema.items():

            if dtype != pl.String:
                continue

            expressions.append(
                pl.col(column)
                .str.strip_chars()
                .str.replace_all(r"\s+", " ")
                .replace("", None)
                .alias(column)
            )

        df = df.with_columns(expressions)

        logger.info("String cleaning completed.")

        return df

    def _validate_primary_key(
        self,
        dataset_name: str,
        df: pl.DataFrame,
    ) -> None:
        """
        Validate primary key(s) for a dataset.
        """

        schema = IMDB_SCHEMAS[dataset_name]
        primary_key = schema["primary_key"]

        if isinstance(primary_key, str):
            primary_key = [primary_key]

        # --------------------------------------------------
        # Validate PK columns exist
        # --------------------------------------------------

        missing_columns = [
            column
            for column in primary_key
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"{dataset_name}: Missing primary key columns: "
                f"{missing_columns}"
            )

        # --------------------------------------------------
        # Metrics
        # --------------------------------------------------

        total_rows = df.height

        null_pk_count = (
            df.filter(
                pl.any_horizontal(
                    [pl.col(col).is_null() for col in primary_key]
                )
            ).height
        )

        duplicate_pk_groups = (
            df.group_by(primary_key)
            .len()
            .filter(pl.col("len") > 1)
            .height
        )

        duplicate_pk_rows = (
            df.group_by(primary_key)
            .len()
            .filter(pl.col("len") > 1)
            .select(pl.col("len").sum())
            .item()
            or 0
        )

        # --------------------------------------------------
        # Logging
        # --------------------------------------------------

        logger.info("=" * 60)
        logger.info(f"Primary Key Validation : {dataset_name}")
        logger.info(f"Primary Key            : {primary_key}")
        logger.info(f"Total Rows             : {total_rows:,}")
        logger.info(f"NULL Primary Keys      : {null_pk_count:,}")
        logger.info(f"Duplicate Key Groups   : {duplicate_pk_groups:,}")
        logger.info(f"Duplicate Rows         : {duplicate_pk_rows:,}")
        logger.info("=" * 60)

        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

        errors = []

        if null_pk_count > 0:
            errors.append(f"{null_pk_count:,} NULL primary keys")

        if duplicate_pk_groups > 0:
            errors.append(f"{duplicate_pk_groups:,} duplicate key groups")

        if errors:
            raise ValueError(
                f"{dataset_name}: Primary key validation failed -> "
                + ", ".join(errors)
            )

        logger.success(
            f"{dataset_name}: Primary key validation passed."
        )