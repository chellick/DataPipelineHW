import asyncio
import logging
import aiohttp

logger = logging.getLogger("YouTubeScraper")
logging.basicConfig(level=logging.INFO)


class YouTubeScraper:
    def __init__(self, video_urls):
        """
        Инициализация скрейпера с предоставленным списком URL видео.
        
        :param video_urls: Список URL для обработки.
        """
        self.video_urls = video_urls

    async def fetch_html(self, url, session):
        """
        Асинхронно загружает HTML по предоставленному URL.
        
        :param url: URL видео.
        :param session: Асинхронная сессия aiohttp.
        :return: HTML содержимое страницы или None, если возникла ошибка.
        """
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    logger.info(f"Successfully fetched HTML for {url}")
                    return html
                else:
                    logger.error(f"Failed to fetch {url}: HTTP {response.status}")
        except asyncio.TimeoutError:
            logger.error(f"Timeout while fetching {url}")
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
        return None

    async def get_video_data(self):
        """
        Загружает HTML всех страниц видео асинхронно.
        
        :return: Список HTML-содержимого страниц или None для URL с ошибками.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_html(url, session) for url in self.video_urls]
            results = await asyncio.gather(*tasks)
            successful = sum(1 for result in results if result is not None)
            logger.info(f"Successfully fetched HTML for {successful}/{len(self.video_urls)} URLs")
            return [result for result in results if result is not None]
