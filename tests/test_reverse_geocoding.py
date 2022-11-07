import pytest
import requests
import checks
import data.geodata


@pytest.mark.reverse
class TestSimpleReverse:
    """Тесты на внутренние ошибки сервера и формат ответа"""

    @pytest.mark.parametrize('extension', ['xml', 'json', 'jsonv2', 'geojson', 'geocodejson'])
    def test_send_request_using_format(self, extension):
        """Проверка, что можно сделать реверсивный запрос с указанием формата"""

        lat = 46
        lon = 20
        url = f'https://nominatim.openstreetmap.org/reverse?format={extension}&lat={lat}&lon={lon}'

        response = requests.get(url)
        checks.status_code(response, 200)
        checks.content_type(response, extension)
        checks.contents_in_response(extension, response)

    def test_send_request_without_format(self):
        """Проверка, что можно сделать реверсивный запрос без указания формата"""

        lat = 20
        lon = 10
        extension = 'without_format'
        url = f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}'

        response = requests.get(url)
        checks.status_code(response, 200)
        checks.content_type(response, extension)
        checks.contents_in_response(extension, response)

    @pytest.mark.parametrize('extension', ['xml', 'json', 'non-existent'])
    @pytest.mark.parametrize("lat, lon", data.geodata.lat_lon)
    def test_send_request_with_incorrect_data(self, lat, lon, extension):
        """Проверка, что на запрос с указанием некорректных lat и lot приходит ошибка"""

        url = f'https://nominatim.openstreetmap.org/reverse?format={extension}&lat={lat}&lon={lon}'

        response = requests.get(url)
        checks.status_code(response, 400)
        checks.content_type(response, extension)
