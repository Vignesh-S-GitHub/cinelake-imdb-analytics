<div align="center">

# CineLake · IMDb Analytics
### A medallion-style data platform for movie and TV datasets

**IMDb ingestion · Polars transformations · Delta Lake · OCI Object Storage**

</div>

CineLake is a data engineering project for ingesting IMDb datasets and shaping them into progressively curated layers. It uses a **Bronze → Silver → Gold** design, with scheduled ingestion through GitHub Actions and Delta Lake storage in Oracle Cloud Infrastructure (OCI) Object Storage.

## Data flow

```text
IMDb source datasets
       │ scheduled ingestion
       ▼
Bronze · raw / landed data
       │ validation and transformation (Polars)
       ▼
Silver · curated Delta tables
       │ analytics and aggregation
       ▼
Gold · analytical outputs (in progress)
       │
OCI Object Storage
```

## Project features

- Weekly automated ingestion configured with GitHub Actions
- Polars-based data processing
- Delta Lake tables for versioned, layered datasets
- DuckDB and analytics components for local exploration
- OCI Object Storage as the remote table store
- Typer CLI with download, Bronze, Silver, and Gold workflow commands; the Gold command is currently disabled in the CLI while that layer evolves

## Technology

| Area | Tools |
|---|---|
| Data processing | Polars, PyArrow |
| Table format and local analytics | Delta Lake, DuckDB |
| Storage | Oracle OCI Object Storage |
| Orchestration and interface | GitHub Actions, Typer |
| Project tooling | Python 3.11+, uv |

## Get started

Install the project environment with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
uv run python -m cinelake.cli --help
```

Configure storage and dataset settings using the examples and documentation in `config/` and `docs/` before running ingestion. Cloud object storage requires your own OCI account and credentials; keep secrets in local environment configuration and never commit them.

## Repository map

- `cinelake/ingestion/` — source dataset acquisition
- `cinelake/bronze/`, `silver/`, `gold/` — medallion processing layers
- `cinelake/analytics/` — analytical logic
- `cinelake/dashboard/` — visualization components
- `config/` — project configuration
- `data/` — local data workspace
- `.github/workflows/` — scheduled automation

## Scope

This is an evolving portfolio project. Cloud costs, source dataset terms, and workflow availability depend on your configuration. Review the repository documentation and workflow settings before enabling scheduled runs.

---

<p align="center"><sub>From raw IMDb data to a clearer view of cinema.</sub></p>
