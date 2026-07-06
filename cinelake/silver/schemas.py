"""
IMDb dataset schemas and Silver layer configuration.

This module defines:
- Expected columns
- Primary key
- Target data types (used in Silver)
- Business validation rules (future)
"""

import polars as pl

IMDB_SCHEMAS = {
    "title_basics": {
        "primary_key": "tconst",
        "columns": [
            "tconst",
            "titleType",
            "primaryTitle",
            "originalTitle",
            "isAdult",
            "startYear",
            "endYear",
            "runtimeMinutes",
            "genres",
            "_ingestion_time",
            "_source_file",
        ],
        "types": {
            "tconst": pl.String,
            "titleType": pl.String,
            "primaryTitle": pl.String,
            "originalTitle": pl.String,
            "isAdult": pl.Boolean,
            "startYear": pl.Int32,
            "endYear": pl.Int32,
            "runtimeMinutes": pl.Int32,
            "genres": pl.String,
        },
        "rules": {
            "runtimeMinutes": {"min": 0},
            "startYear": {"min": 1874},
            "endYear": {"nullable": True},
        },
    },

    "title_ratings": {
        "primary_key": "tconst",
        "columns": [
            "tconst",
            "averageRating",
            "numVotes",
            "_ingestion_time",
            "_source_file",
        ],
        "types": {
            "tconst": pl.String,
            "averageRating": pl.Float64,
            "numVotes": pl.Int64,
        },
        "rules": {
            "averageRating": {"min": 0, "max": 10},
            "numVotes": {"min": 0},
        },
    },

    "title_crew": {
        "primary_key": "tconst",
        "columns": [
            "tconst",
            "directors",
            "writers",
            "_ingestion_time",
            "_source_file",
        ],
        "types": {
            "tconst": pl.String,
            "directors": pl.String,
            "writers": pl.String,
        },
        "rules": {},
    },

    "title_principals": {
        "primary_key": ["tconst", "ordering"],
        "columns": [
            "tconst",
            "ordering",
            "nconst",
            "category",
            "job",
            "characters",
            "_ingestion_time",
            "_source_file",
        ],
        "types": {
            "tconst": pl.String,
            "ordering": pl.Int32,
            "nconst": pl.String,
            "category": pl.String,
            "job": pl.String,
            "characters": pl.String,
        },
        "rules": {},
    },

    "title_episode": {
        "primary_key": "tconst",
        "columns": [
            "tconst",
            "parentTconst",
            "seasonNumber",
            "episodeNumber",
            "_ingestion_time",
            "_source_file",
        ],
        "types": {
            "tconst": pl.String,
            "parentTconst": pl.String,
            "seasonNumber": pl.Int32,
            "episodeNumber": pl.Int32,
        },
        "rules": {},
    },

    "title_akas": {
        "primary_key": ["titleId", "ordering"],
        "columns": [
            "titleId",
            "ordering",
            "title",
            "region",
            "language",
            "types",
            "attributes",
            "isOriginalTitle",
            "_ingestion_time",
            "_source_file",
        ],
        "types": {
            "titleId": pl.String,
            "ordering": pl.Int32,
            "title": pl.String,
            "region": pl.String,
            "language": pl.String,
            "types": pl.String,
            "attributes": pl.String,
            "isOriginalTitle": pl.Boolean,
        },
        "rules": {},
    },

    "name_basics": {
        "primary_key": "nconst",
        "columns": [
            "nconst",
            "primaryName",
            "birthYear",
            "deathYear",
            "primaryProfession",
            "knownForTitles",
            "_ingestion_time",
            "_source_file",
        ],
        "types": {
            "nconst": pl.String,
            "primaryName": pl.String,
            "birthYear": pl.Int32,
            "deathYear": pl.Int32,
            "primaryProfession": pl.String,
            "knownForTitles": pl.String,
        },
        "rules": {},
    },
}