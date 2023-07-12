import unittest
from unittest.mock import patch, Mock
from crawler import Crawler

class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler()

    def test_normalize_url(self):
        url = 'HTTPS://www.J-Archive.com/ShowGame.php?game_id=6455'
        normalized_url = self.crawler.normalize_url(url)
        self.assertEqual(normalized_url, 'https://www.j-archive.com/showgame.php?game_id=6455')

    def test_filter_url(self):
        valid_url = 'https://www.j-archive.com/showgame.php?game_id=6455'
        invalid_url = 'https://www.j-archive.com/otherpage.php'
        self.assertTrue(self.crawler.filter_url(valid_url))
        self.assertFalse(self.crawler.filter_url(invalid_url))

    @patch('crawler.requests.get')
    def test_crawl_page(self, mock_get):
        mock_response = Mock()
        mock_response.headers = {"content-type": "text/html"}
        mock_get.return_value = mock_response

        url = 'https://www.j-archive.com/showgame.php?game_id=6455'
        self.crawler.crawl(url)

        # Verify that the page was crawled and added to pages_crawled
        self.assertIn(url, self.crawler.pages_crawled)

if __name__ == '__main__':
    unittest.main()
