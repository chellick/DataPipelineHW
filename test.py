import logging
from bs4 import BeautifulSoup
from pprint import pprint

# Настройка логирования
logging.basicConfig(level=logging.INFO)

class YouTubeParser:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    async def parse(self, html_content):
        if not html_content:
            self.logger.info("No HTML content to parse")
            return {}

        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Извлечение метаданных
            title = self._get_title(soup)
            description = self._get_description(soup)
            tags = self._get_tags(soup)
            channel_name = self._get_channel_name(soup)
            views_number = self._get_views_number(soup)
            upload_date = self._get_upload_date(soup)
            genre = self._get_genre(soup)

            video_data = {
                'title': title,
                'description': description,
                'tags': tags,
                'channel_name': channel_name,
                'views_number': views_number,
                'upload_date': upload_date,
                'genre': genre
            }

            self.logger.info("Successfully parsed video data")
            return video_data

        except Exception as e:
            self.logger.error(f"Error parsing HTML content: {e}")
            return {}

    def _get_title(self, soup):
        title_tag = soup.find('meta', {'name': 'title'})
        return title_tag['content'] if title_tag else ''

    def _get_description(self, soup):
        description_tag = soup.find('meta', {'name': 'description'})
        return description_tag['content'] if description_tag else ''

    def _get_tags(self, soup):
        tags_tag = soup.find('meta', {'name': 'keywords'})
        return tags_tag['content'].split(',') if tags_tag else []

    def _get_channel_name(self, soup):
        channel_tag = soup.find('link', {'itemprop': 'name'})
        return channel_tag['content'] if channel_tag else ''

    def _get_views_number(self, soup):
        views_tag = soup.find('meta', {'itemprop': 'interactionCount'})
        return views_tag['content'] if views_tag else ''

    def _get_upload_date(self, soup):
        upload_date_tag = soup.find('meta', {'itemprop': 'uploadDate'})
        return upload_date_tag['content'] if upload_date_tag else ''

    def _get_genre(self, soup):
        genre_tag = soup.find('meta', {'itemprop': 'genre'})
        return genre_tag['content'] if genre_tag else ''

# Пример использования
async def main():
    html_content = '''
    <html>
        <head>
            <meta name="title" content="Пример видео">
            <meta name="description" content="Описание видео">
            <meta name="keywords" content="Tag1,Tag2">
            <link itemprop="name" content="Название канала">
            <meta itemprop="interactionCount" content="123456">
            <meta itemprop="uploadDate" content="2024-10-10">
            <meta itemprop="genre" content="Жанр видео">
        </head>
        <body>
            <!-- Содержимое страницы -->
        </body>
    </html>
    '''
    parser = YouTubeParser()
    video_data = await parser.parse(html_content)
    pprint(video_data)

# Запуск асинхронного примера
import asyncio
asyncio.run(main())
