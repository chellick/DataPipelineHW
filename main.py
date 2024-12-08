import asyncio
import logging
from gsw import GoogleSheetWriter
from config.settings import SPREADSHEET_ID

logging.basicConfig(level=logging.INFO)

async def main():
    writer = GoogleSheetWriter(SPREADSHEET_ID)

    print(writer.__dict__)

    video_data = [
        {
            'title': 'Пример видео 1',
            'description': 'Описание первого видео',
            'tags': ['Tag1', 'Tag2', 'Tag3'],
            'channel_name': 'Канал 1',
            'views_number': '123456',
            'upload_date': '2024-12-01',
            'genre': 'Жанр 1'
        },
        {
            'title': 'Пример видео 2',
            'description': 'Описание второго видео',
            'tags': ['TagA', 'TagB'],
            'channel_name': 'Канал 2',
            'views_number': '654321',
            'upload_date': '2024-12-02',
            'genre': 'Жанр 2'
        }
    ]

    await writer.write_to_sheet(video_data)

if __name__ == "__main__":
    asyncio.run(main())
