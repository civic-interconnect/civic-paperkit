from civic_interconnect.paperkit.scrape import extract_links

HTML = """
<html>
  <body>
    <a href="/files/data1.csv">Data 1</a>
    <a href="/files/report.pdf">Report</a>
    <a href="/files/readme.txt">Ignore</a>
  </body>
</html>
"""


def test_extract_links_filters_by_ext():
    links = extract_links(HTML, "https://example.org/base/", [".csv", ".pdf"], None)
    assert links == [
        "https://example.org/files/data1.csv",
        "https://example.org/files/report.pdf",
    ]
