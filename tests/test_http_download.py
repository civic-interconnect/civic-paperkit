from pathlib import Path

import requests
import responses

from civic_interconnect.paperkit.download import download_file
from civic_interconnect.paperkit.http_client import HttpClient


@responses.activate
def test_download_file(tmp_path: Path):
    url = "https://example.org/a.csv"
    responses.add(responses.GET, url, body="x,y\n1,2\n", status=200)

    client = HttpClient(session=requests.Session(), retries=1)
    out = tmp_path / "a.csv"
    p = download_file(client, url, out)
    assert p.exists()
    assert p.read_text() == "x,y\n1,2\n"
