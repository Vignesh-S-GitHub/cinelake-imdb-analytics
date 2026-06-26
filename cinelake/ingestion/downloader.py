from pathlib import Path

import httpx
from loguru import logger
from rich.progress import track

from cinelake.config.settings import Settings


class IMDbDownloader:
    """
    Download IMDb datasets from IMDb public dataset endpoint.
    """

    def __init__(self, settings: Settings):
        self.settings = settings

        self.download_dir = Path("data/raw")
        self.download_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = httpx.Client(
            timeout=self.settings.timeout_seconds,
            follow_redirects=True,
        )

    def build_url(self, filename: str) -> str:
        """
        Build dataset URL.
        """
        return f"{self.settings.base_url}/{filename}"

    def download_file(self, filename: str) -> Path:
        """
        Download a single IMDb dataset.
        """

        url = self.build_url(filename)

        destination = self.download_dir / filename

        if destination.exists():
            logger.info(
                f"Skipping existing file: {filename}"
            )
            return destination

        logger.info(
            f"Downloading {filename}"
        )

        for attempt in range(
            1,
            self.settings.max_retries + 1,
        ):
            try:
                with self.client.stream(
                    "GET",
                    url,
                ) as response:

                    response.raise_for_status()

                    with open(
                        destination,
                        "wb",
                    ) as file:

                        for chunk in response.iter_bytes(
                            self.settings.chunk_size
                        ):
                            file.write(chunk)

                if destination.stat().st_size == 0:
                    raise ValueError(
                        f"{filename} downloaded as empty file."
                    )

                logger.success(
                    f"Downloaded {filename}"
                )

                return destination

            except Exception as exc:
                logger.warning(
                    f"Attempt {attempt}/"
                    f"{self.settings.max_retries} "
                    f"failed for {filename}: {exc}"
                )

        raise RuntimeError(
            f"Failed to download {filename}"
        )

    def download_all(self) -> list[Path]:
        """
        Download all IMDb datasets.
        """

        downloaded_files: list[Path] = []

        logger.info(
            "Starting IMDb dataset download process"
        )

        for filename in track(
            self.settings.datasets.values(),
            description="Downloading IMDb datasets...",
        ):
            downloaded_files.append(
                self.download_file(filename)
            )

        logger.success(
            f"Downloaded "
            f"{len(downloaded_files)} datasets"
        )

        return downloaded_files

    def close(self) -> None:
        """
        Close HTTP client.
        """
        self.client.close()

if __name__ == "__main__":
    print("Downloader module loaded")