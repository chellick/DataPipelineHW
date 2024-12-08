import asyncio
import logging
from gsw import GoogleSheetWriter, parser, scraper
from config.settings import SPREADSHEET_ID

logging.basicConfig(level=logging.INFO)

async def main():
    url = input("Введите URL YouTube видео: ")
    
    scr = scraper.YouTubeScraper([url])
    par = parser.YouTubeParser()
    
    try:
        video_data = await scr.get_video_data()
        if not video_data:
            logging.error("Не удалось получить данные о видео. Проверьте URL.")
            return
    except Exception as e:
        logging.error(f"Ошибка при скрапинге данных: {e}")
        return
    
    try:
        parsed = await par.parse(video_data[0])
        logging.info("Данные успешно распарсены.")
    except Exception as e:
        logging.error(f"Ошибка при парсинге данных: {e}")
        return

    print("Распарсенные данные о видео:")
    for key, value in parsed.items():
        print(f"{key}: {value}")
    
    try:
        sw = GoogleSheetWriter(spreadsheet_id=SPREADSHEET_ID)
        await sw.write_to_sheet([parsed])
        logging.info("Данные успешно сохранены в Google Sheets.")
    except Exception as e:
        logging.error(f"Ошибка при сохранении данных в Google Sheets: {e}")

if __name__ == "__main__":
    asyncio.run(main())
