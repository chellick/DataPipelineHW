import asyncio
import logging
from gsw import GoogleSheetWriter, YouTubeParser, YouTubeScraper
from config.settings import SPREADSHEET_ID

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class YouTubePipeline:
    def __init__(self, scraper, parser, writer):
        """
        Инициализация конвейера.
        
        :param scraper: Экземпляр YouTubeScraper для загрузки данных.
        :param parser: Экземпляр YouTubeParser для парсинга данных.
        :param writer: Экземпляр GoogleSheetWriter для записи данных.
        """
        self.scraper = scraper
        self.parser = parser
        self.writer = writer

    async def run(self, spreadsheet_id):
        """
        Запуск конвейера с обработкой ошибок.
        
        :param video_urls: Список URL YouTube видео.
        :param spreadsheet_id: Идентификатор Google Sheets.
        """
        logger.info("Запуск конвейера данных YouTube...")

        


        try:
            logger.info("Загрузка данных о видео...")
            
            video_data = await self.scraper.get_video_data()
            
            if not video_data:
                logger.error("Не удалось загрузить данные ни для одного видео. Проверьте URL.")
                return

            logger.info("Все доступные данные о видео успешно загружены.")
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке данных: {e}")
            return

        try:
            logger.info("Парсинг данных...")
            parsed_data = [await self.parser.parse(video) for video in video_data]
            print(parsed_data)
            logger.info("Данные успешно распарсены.")
        except Exception as e:
            logger.error(f"Ошибка при парсинге данных: {e}")
            return

        try:
            logger.info("Запись данных в Google Sheets...")
            self.writer.sheet_id = spreadsheet_id
            await self.writer.write_to_sheet(parsed_data)
            logger.info("Данные успешно сохранены в Google Sheets.")
        except Exception as e:
            logger.error(f"Ошибка при записи данных в Google Sheets: {e}")
            return

        logger.info("Конвейер успешно завершён!")


if __name__ == "__main__":


    async def main():
        
        video_urls = [
                'https://www.youtube.com/watch?v=ModFC1bhobA',
                # 'https://www.youtube.com/watch?v=SIm2W9TtzR0',
        ]
        
        spreadsheet_id = SPREADSHEET_ID

        scraper = YouTubeScraper(video_urls)
        parser = YouTubeParser()
        writer = GoogleSheetWriter(spreadsheet_id) 

        pipeline = YouTubePipeline(scraper, parser, writer)
        await pipeline.run(spreadsheet_id)

    asyncio.run(main())


