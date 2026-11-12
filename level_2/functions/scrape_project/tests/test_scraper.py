from scraper import scrape_title

def test_scrape_title_success():
    """Test that the scraper can succesfully parte a title"""
    # We use a local server or a reliable site for real test
    # but for this example, we'll mock or use a known static site
    test_url="http://info.cern.ch" # The first website
    title=scrape_title(test_url)
    assert title is not None
    assert isinstance(title,str)
