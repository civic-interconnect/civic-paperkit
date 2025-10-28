from pathlib import Path

from civic_interconnect.paperkit.bib import load_bib_keys


def test_load_bib_keys(tmp_path: Path):
    bib = tmp_path / "refs.bib"
    bib.write_text("@article{key1, title={T}}\n@misc{key2, howpublished={x}}", encoding="utf-8")
    keys = load_bib_keys(bib)
    assert set(keys) == {"key1", "key2"}
