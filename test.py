from gspread_asyncio import AsyncioGspreadClientManager
from oauth2client.service_account import ServiceAccountCredentials

def get_creds():
    from config.settings import SERVICE_ACCOUNT_FILE
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    return ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)

async def test_access():
    agcm = AsyncioGspreadClientManager(get_creds)
    agc = await agcm.authorize()
    sheet = await agc.open_by_key('1bXChmONwvcoKGuEKCiuS3w3cYu67wTu7vw-UgjT-ppo')
    worksheet = await sheet.get_worksheet(0)
    print(f"Название листа: {worksheet.title}")

import asyncio
asyncio.run(test_access())
