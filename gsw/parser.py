import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("YouTubeParser")
logging.basicConfig(level=logging.INFO)

class YouTubeParser:
    async def parse(self, html_content):
        """
        Асинхронно парсит HTML страницы и извлекает метаданные.
        
        :param html_content: HTML содержимое страницы (str).
        :return: Словарь с метаданными видео (dict).
        """
        if not html_content:
            logging.warning("Нет HTML-контента для парсинга.")
            return {}

        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            data = {
                'title': self.safe_find(soup, 'meta', {'name': 'title'}, 'content'),
                'description': self.safe_find(soup, 'meta', {'name': 'description'}, 'content'),
                'tags': [tag['content'] for tag in soup.find_all('meta', property='og:video:tag')],
                'channel_name': self.safe_find(soup, 'meta', {'itemprop': 'author'}, 'content'),
                'views_number': self.safe_find(soup, 'meta', {'itemprop': 'interactionCount'}, 'content', convert=int),
                'upload_date': self.safe_find(soup, 'meta', {'itemprop': 'uploadDate'}, 'content'),
                'genre': self.safe_find(soup, 'meta', {'itemprop': 'genre'}, 'content'),
            }

            # Логирование успеха
            logging.info("Успешно извлечены данные о видео.")
            return data

        except Exception as e:
            logging.error(f"Ошибка парсинга HTML: {e}")
            return {}

    @staticmethod
    def safe_find(soup, tag, attrs, attribute, convert=None):
        """
        Безопасно ищет элемент в HTML с заданными параметрами.
        
        :param soup: Объект BeautifulSoup.
        :param tag: Название тега (str).
        :param attrs: Атрибуты для поиска (dict).
        :param attribute: Атрибут, значение которого нужно извлечь (str).
        :param convert: Функция для преобразования значения (например, int).
        :return: Значение атрибута или None.
        """
        try:
            element = soup.find(tag, attrs=attrs)
            if element and attribute in element.attrs:
                return convert(element[attribute]) if convert else element[attribute]
        except Exception as e:
            logging.warning(f"Ошибка поиска {tag} с атрибутами {attrs}: {e}")
        return None
