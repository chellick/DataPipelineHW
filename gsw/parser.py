import asyncio
import requests
import bs4
import aiohttp
import asyncio
import logging
import pprint
from bs4 import BeautifulSoup



logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

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
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    logger.info(f"Successfully fetched HTML for {url}")
                    return html
                else:
                    logger.error(f"Failed to fetch {url}: HTTP {response.status}")
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
        return results


# urls = [
#     "https://youtu.be/M2a1eZy5zmI?si=c_LS3liTswB4FF2L",
#     "https://www.youtube.com/live/IWDTBX_Vk5Q?si=U6HqWUKse-VE4PKB",
#     "https://youtu.be/t7pHGNyHbu4?si=St7qOZOfBVmVFC-E"
# ]
# scraper = YouTubeScraper(urls)



# async def main():
#     video_data = await scraper.get_video_data()
#     for i, data in enumerate(video_data):
#         print(f"Video {i + 1}: {'HTML fetched' if data else 'Failed to fetch'}")
#         print(data)
#         break

# asyncio.run(main())
