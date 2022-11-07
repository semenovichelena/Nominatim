import pytest
import requests
import checks
import data.geodata


@pytest.mark.search
class TestSimpleSearch:
    """Тесты на внутренние ошибки сервера и формат ответа"""

    @pytest.mark.parametrize('query', ['Исаакиевский собор Санкт-Петербург', 'Африка', 'moscow', 'Ленинский,79', '15'])
    @pytest.mark.parametrize('extension', ['xml', 'json', 'jsonv2', 'geojson', 'geocodejson'])
    def test_send_request_using_format(self, query, extension):
        """Проверка, что можно сделать прямой запрос с указанием формата и различными запросами"""

        url = f'https://nominatim.openstreetmap.org/?q={query}&format={extension}'

        response = requests.get(url)
        checks.status_code(response, 200)
        checks.content_type(response, extension)
        checks.validation_response_search(response, extension)

    def test_send_request_with_incorrect_format(self):
        """Проверка, что получаем ошибку при указании неверного формата"""

        query = 'Исаакиевский собор Санкт-Петербург'
        extension = 'non-existent'
        url = f'https://nominatim.openstreetmap.org/?q={query}&format={extension}'

        response = requests.get(url)
        checks.status_code(response, 400)
        checks.content_type(response, extension)

    @pytest.mark.parametrize("street, city, county, state, country, postalcode", data.geodata.addresses)
    @pytest.mark.parametrize('extension', ['xml', 'json', 'jsonv2', 'geojson', 'geocodejson'])
    def test_send_structured_request_using_format(self, street, city, county, state, country, postalcode, extension):
        """Проверка, что можно сделать прямой структурированный запрос с указанием формата и различными данными"""

        url = f'https://nominatim.openstreetmap.org/search/?{street}{city}{county}{state}{country}{postalcode}format={extension}'

        response = requests.get(url)
        checks.status_code(response, 200)
        checks.content_type(response, extension)
        checks.validation_response_search(response, extension)
