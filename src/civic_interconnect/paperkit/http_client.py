"""HTTP client wrapper for making GET requests with retries and logging.

This module provides the HttpClient dataclass for robust HTTP GET requests,
including configurable timeout, retries, backoff, and user-agent.

File: src/civic_interconnect/paperkit/http_client.py
"""

from dataclasses import dataclass
import time

import requests

from .log import logger


@dataclass
class HttpClient:
    """HTTP client for making GET requests with retries, backoff, and custom user-agent.

    Attributes
    ----------
    session : requests.Session
        The requests session used for HTTP requests.
    timeout : int
        Timeout for each request in seconds.
    retries : int
        Number of retry attempts for failed requests.
    backoff_seconds : int
        Base seconds to wait between retries (multiplied by attempt number).
    user_agent : str
        User-Agent header for requests.
    """

    session: requests.Session
    timeout: int = 30
    retries: int = 3
    backoff_seconds: int = 2
    user_agent: str = "ci-paper-fetcher/1.0"

    def get(self, url: str) -> requests.Response:
        """Perform an HTTP GET request with retries and exponential backoff.

        Parameters
        ----------
        url : str
            The URL to send the GET request to.

        Returns
        -------
        requests.Response
            The HTTP response object.

        Raises
        ------
        Exception
            If all retry attempts fail, the last exception is raised.
        """
        last_exc: Exception | None = None
        headers = {"User-Agent": self.user_agent}
        for attempt in range(1, self.retries + 1):
            try:
                logger.debug("HTTP GET %s (attempt %s)", url, attempt)
                resp = self.session.get(url, timeout=self.timeout, headers=headers)
                resp.raise_for_status()
                return resp
            except Exception as exc:
                logger.warning("HTTP GET failed for %s on attempt %s: %s", url, attempt, exc)
                last_exc = exc
                if attempt < self.retries:
                    time.sleep(self.backoff_seconds * attempt)
        logger.error("HTTP GET giving up for %s", url)
        raise last_exc if last_exc else RuntimeError("HTTP get failed unexpectedly")
