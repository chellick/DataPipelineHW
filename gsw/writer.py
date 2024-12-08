import logging
from gspread_asyncio import AsyncioGspreadClientManager
from oauth2client.service_account import ServiceAccountCredentials

logger = logging.getLogger("GoogleSheetWriter")

class GoogleSheetWriter:
    def __init__(self, spreadsheet_id, worksheet_name='YouTube Data'):
        self.sheet_id = spreadsheet_id
        self.worksheet_name = worksheet_name
        self.sheet = None
        self.agcm = AsyncioGspreadClientManager(self.get_creds)

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
            self.sheet = await spreadsheet.worksheet(self.worksheet_name)
            logger.info(f"Initialized spreadsheet '{self.sheet_id}'")
        except Exception as e:
            logger.error(f"Error initializing spreadsheet: {e}")
            raise

    async def write_to_sheet(self, data):
        if not self.sheet:
            await self.init_spreadsheet()

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
            await self.sheet.clear()
            await self.sheet.append_rows(rows)
            logger.info("Data written to sheet.")
        except Exception as e:
            logger.error(f"Error writing to sheet: {e}")
            raise
