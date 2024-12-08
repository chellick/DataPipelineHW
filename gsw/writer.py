import logging
from gspread_asyncio import AsyncioGspreadClientManager
from oauth2client.service_account import ServiceAccountCredentials

logger = logging.getLogger("GoogleSheetWriter")
logging.basicConfig(level=logging.INFO)


class GoogleSheetWriter:
    def __init__(self, spreadsheet_id):
        self.sheet_id = spreadsheet_id
        self.agcm = AsyncioGspreadClientManager(self.get_creds)
        self.worksheet = None

    @staticmethod
    def get_creds():
        from config.settings import SERVICE_ACCOUNT_FILE  # Путь к JSON-файлу
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        return ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)

    async def init_spreadsheet(self):
        try:
            agc = await self.agcm.authorize()
            spreadsheet = await agc.open_by_key(self.sheet_id)
            self.worksheet = await spreadsheet.get_worksheet(0)  # Получаем первый лист
            logger.info(f"Initialized spreadsheet '{self.sheet_id}'")
        except Exception as e:
            logger.error(f"Error initializing spreadsheet: {e}")
            logger.exception(e)  # Добавлено для вывода полного стека ошибки
            raise

    async def write_to_sheet(self, data):
        if not self.worksheet:
            await self.init_spreadsheet()

        # Формируем строки для записи
        rows = [['Title', 'Description', 'Tags', 'Channel Name', 'Views Number', 'Upload Date', 'Genre']]
        for video in data:
            rows.append([
                video.get('title', ''),
                video.get('description', ''),
                ', '.join(video.get('tags', [])),
                video.get('channel_name', ''),
                video.get('views_number', ''),
                video.get('upload_date', ''),
                video.get('genre', ''),
            ])

        try:
            # Очистка и запись данных
            await self.worksheet.clear()
            await self.worksheet.append_rows(rows)
            logger.info("Data successfully written to sheet.")
        except Exception as e:
            logger.error(f"Error writing to sheet: {e}")
            logger.exception(e)  # Добавлено для вывода полного стека ошибки
            raise
