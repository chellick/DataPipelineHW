import logging
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeParser:
    async def parse(self, html_content):
        if not html_content:
            logger.warning("No HTML content to parse")
            return {}

        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            title = soup.find('meta', attrs={'name': 'title'})
            description = soup.find('meta', attrs={'name': 'description'})
            channel_name = soup.find('link', itemprop='name')
            views_number = soup.find('meta', itemprop='interactionCount')
            upload_date = soup.find('meta', itemprop='uploadDate')
            genre = soup.find('meta', itemprop='genre')
            tags = [tag['content'] for tag in soup.find_all('meta', property='og:video:tag')]

            video_data = {
                'title': title['content'] if title else None,
                'description': description['content'] if description else None,
                'tags': tags,
                'channel_name': channel_name['content'] if channel_name else None,
                'views_number': views_number['content'] if views_number else None,
                'upload_date': upload_date['content'] if upload_date else None,
                'genre': genre['content'] if genre else None
            }

            logger.info("Successfully parsed video data")
            return video_data

        except Exception as e:
            logger.error(f"Error parsing HTML content: {e}")
            return {}
