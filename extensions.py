import requests
import json


class APIException(Exception):
    """Пользовательское исключение для ошибок API."""
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        """
        Конвертирует валюту через API.
        :param base: Валюта для конвертации (например, 'USD').
        :param quote: Валюта, в которую конвертируем (например, 'EUR').
        :param amount: Количество валюты.
        :return: Результат конвертации.
        """
        # API для получения курса валют: https://www.exchangerate-api.com
        url = f"https://api.exchangerate-api.com/v4/latest/{base.upper()}"

        try:
            response = requests.get(url)
            data = json.loads(response.text)

            if response.status_code != 200:
                raise APIException(f"Ошибка API: {data.get('error', 'Неизвестная ошибка')}")

            if quote.upper() not in data['rates']:
                raise APIException(f"Валюта {quote} не найдена!")

            rate = data['rates'][quote.upper()]
            return round(rate * amount, 2)

        except requests.exceptions.RequestException as e:
            raise APIException(f"Ошибка соединения: {e}")
        except json.JSONDecodeError:
            raise APIException("Ошибка обработки данных API")