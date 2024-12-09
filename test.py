#Шаг 1
import asyncio
import aiohttp
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

class YouTubeScraper:

    def __init__(self, video_urls):
        self.video_urls = video_urls

    async def fetch_html(self, url, session):
        async with session.get(url) as response:
            if response.status == 200:
                print(f'Successfully fetched HTML for {url}')
                html = await response.text()  # Получаем HTML-код страницы
                return html
            else:
                print(f'Ошибка: {response.status}')

    async def get_video_data(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_html(url = url, session=session) for url in self.video_urls]
            results = await asyncio.gather(*tasks)
            return results

#Шаг 2
from bs4 import BeautifulSoup

class YouTubeParser:
    async def parse(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        try:
            title = soup.find('meta', attrs = {'name': 'title'})['content']
            description = soup.find('meta', attrs = {'name': 'description'})['content']
            channel_name = soup.find('link', itemprop='name')['content']
            tags = [tag['content'] for tag in soup.find_all('meta', property='og:video:tag')]
            views_number = soup.find('meta', itemprop='interactionCount')['content']
            upload_date = soup.find('meta', itemprop='uploadDate')['content']
            genre = soup.find('meta', itemprop='genre')['content']

            data = {'title': title, 'description': description,
                    'channel_name': channel_name, 'tags': tags,
                    'views_number': views_number, 'upload_date': upload_date,
                    'genre': genre
                    }
 
            return data
        except Exception as e:
            print(f'Произошла ошибка: {e}')

class GoogleSheetWriter:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def __init__(self, spreadsheet_id, worksheet_name='YoutubeData'):
        self.spreadsheet_id = spreadsheet_id
        self.worksheet_name = worksheet_name
        self.creds = self.get_creds()  # Сохраняем учетные данные
        self.sheet = build('sheets', 'v4', credentials=self.creds)  # Создаем объект API

    def get_creds(self):
        '''Аутентификация и получение сервиса для работы с Google Sheets API'''
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return creds  # Возвращаем учетные данные

    async def init_spreadsheet(self):
        try:
            print(f'Initialized spreadsheet {self.spreadsheet_id}')
            return self.sheet.spreadsheets()  # Возвращаем объект для работы с таблицами
            
        except HttpError as err:
            print(f'Ошибка инициализации: {err}')

    async def write_to_sheet(self, data):
        '''Запись данных в таблицу'''
        try:
            sheet = await self.init_spreadsheet()
            if sheet is None:
                return

            # Подготовка данных для записи
            body = {
                'values': [[
                    video['title'],
                    video['description'],
                    ', '.join(video['tags']),
                    video['channel_name'],
                    video['views_number'],
                    video['upload_date'],
                    video['genre']
                ] for video in data]
            }

            # Запись данных в указанный диапазон
            async with aiohttp.ClientSession() as session:
                url = f'https://sheets.googleapis.com/v4/spreadsheets/{self.spreadsheet_id}/values/{self.worksheet_name}!A1?valueInputOption=RAW'
                async with session.put(url, json=body, headers={'Authorization': f'Bearer {self.creds.token}'}) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f'Data written to sheet.')
                    else:
                        print(f'Ошибка записи данных: {response.status} - {await response.text()}')

        except HttpError as err:
            print(f'Ошибка записи данных: {err}')

class YouTubeDataPipeline:
    def __init__(self, video_urls, spreadsheet_id):
        self.scraper = YouTubeScraper(video_urls=video_urls)
        self.parser = YouTubeParser()
        # self.writer = GoogleSheetWriter(spreadsheet_id=spreadsheet_id, worksheet_name='Sheet1')  

    async def run(self):
        try:
            print('Starting YouTube data pipeline...')
            video_data = await self.scraper.get_video_data()
            data = [await self.parser.parse(html_content=i) for i in video_data]
            
            print(data)
            # await self.writer.write_to_sheet(data=data)
            print('Pipeline completed!')
        except Exception as e:
            print(f'Произошла ошибка: {e}')
        

async def main1():

    video_urls = [
    'https://www.youtube.com/watch?v=NSDdJeCmXXE',
    'https://www.youtube.com/watch?v=WGsMydFFPMk'
]
    spreadsheet_id = '12DYIFPUTG7OEC5gLdKwpJhx2FNhK2et8AjtbAU4Z1-c'

    pipeline = YouTubeDataPipeline(video_urls, spreadsheet_id)
    await pipeline.run()

asyncio.run(main1())
