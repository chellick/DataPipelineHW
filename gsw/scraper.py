import asyncio
import logging
import aiohttp



class YouTubeScraper:
    def __init__(self, video_urls):
        """
        Инициализация скрейпера с предоставленным списком URL видео.
        
        :param video_urls: Список URL для обработки.
        """

        self.video_urls = video_urls
        self.logger = logging.getLogger(self.__class__.__name__)

    async def fetch_html(self, url, session):
        """
        Асинхронно загружает HTML по предоставленному URL.
        
        :param url: URL видео.
        :param session: Асинхронная сессия aiohttp.
        :return: HTML содержимое страницы или None, если возникла ошибка.
        """
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                html_content = await response.text()
                self.logger.info(f"Successfully fetched HTML for {url}")
                return html_content
        except Exception as e:
            self.logger.error(f"Failed to fetch {url}: {e}")
            return None

    async def get_video_data(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_html(url, session) for url in self.video_urls]
            return await asyncio.gather(*tasks)