from pathlib import Path

import requests
import responses

from civic_interconnect.paperkit.http_client import HttpClient
from civic_interconnect.paperkit.orchestrate import run


@responses.activate
def test_run_downloads_direct_and_scraped(tmp_path: Path):
    # Fake .bib
    bib = tmp_path / "refs.bib"
    bib.write_text("@misc{alpha, title={A}}\n@misc{beta, title={B}}\n", encoding="utf-8")

    # Meta
    meta = tmp_path / "refs_meta.yaml"
    meta.write_text(
        "alpha:\n"
        "  assets:\n"
        "    - url: https://ex.org/a.csv\n"
        "beta:\n"
        "  assets:\n"
        "    - page_url: https://ex.org/page\n"
        "      allow_ext: ['.csv']\n",
        encoding="utf-8",
    )

    # Network fixtures
    responses.add(responses.GET, "https://ex.org/a.csv", body="id\n1\n", status=200)
    page_html = '<a href="/dl/data.csv">csv</a><a href="/dl/note.txt">txt</a>'
    responses.add(responses.GET, "https://ex.org/page", body=page_html, status=200)
    responses.add(responses.GET, "https://ex.org/dl/data.csv", body="k\n9\n", status=200)

    client = HttpClient(session=requests.Session(), retries=1)
    summary = run(bib, meta, tmp_path / "out", client)

    saved = [str(p) for rec in summary.processed for p in rec.paths]
    assert any(p.replace("\\", "/").endswith("alpha/a.csv") for p in saved)
    assert any(p.replace("\\", "/").endswith("beta/data.csv") for p in saved)
