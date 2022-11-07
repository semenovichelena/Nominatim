import pytest
import requests
import checks


@pytest.mark.connection
class TestConnectionToNominatim:
    """Проверка, запущена ли служба и база данных"""

    def test_checking_service_and_database_text(self):
        """Проверка, запущена ли служба и база данных, status_code в text """

        extension = 'text'
        url = 'https://nominatim.openstreetmap.org/status.php'

        response = requests.get(url)
        checks.status_code(response, 200)
        checks.content_type(response, extension)

    def test_checking_service_and_database_json(self):
        """Проверка, запущена ли служба и база данных, status_code в json """

        extension = 'json'
        url = 'https://nominatim.openstreetmap.org/status.php?format=json'

        response = requests.get(url)
        json = response.json()
        checks.status_code(response, 200)
        checks.content_type(response, extension)
        checks.connection_response_successful(json)

