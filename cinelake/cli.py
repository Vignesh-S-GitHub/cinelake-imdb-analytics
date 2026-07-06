import typer

from cinelake.config.logger import configure_logger
from cinelake.config.settings import load_settings
from cinelake.ingestion.downloader import IMDbDownloader
from cinelake.bronze.bronze_processor import BronzeProcessor
from cinelake.silver.silver_processor import SilverProcessor

configure_logger()

app = typer.Typer(
    help="CineLake IMDb Analytics Platform",
    no_args_is_help=True,
)

@app.command()
def download():
    """Download IMDb datasets."""
    settings = load_settings()
    downloader = IMDbDownloader(settings)
    downloader.download_all()


@app.command()
def bronze():
    """Process raw IMDb datasets into Bronze Delta tables."""
    settings = load_settings()
    processor = BronzeProcessor(settings)
    processor.process_all()


@app.command()
def silver():
    """
    Process Bronze Delta tables into Silver Delta tables.
    """
    settings = load_settings()
    processor = SilverProcessor(settings)
    processor.process_all()


@app.command()
def gold():
    """
    Process Silver Delta tables into Gold Delta tables.
    """
    settings = load_settings()
    #processor = GoldProcessor(settings)
    #processor.process_gold()


if __name__ == "__main__":
    app()
