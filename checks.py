import data.extensions as ext
import data.models_json
import xml.etree.ElementTree as ET
from pydantic import parse_obj_as, ValidationError

from typing import List


def content_type(response, extension):
    expected_result = ext.get_field_by_extension(extension, 'content_type')
    actual_result = response.headers['Content-Type']
    assert expected_result in actual_result, f"Полученный Content-Type не соответствует ожидаемому:" \
                                             f"\nexpected result = '{expected_result}'," \
                                             f"\nactual result = '{actual_result}'"


def status_code(response, expected_result):
    actual_result = response.status_code
    assert actual_result == expected_result, f"Полученный status-code не соответствует ожидаемому: " \
                                             f"\nexpected result = '{expected_result}', " \
                                             f"\nactual result = '{actual_result}'"


def validation_response_search(response, extension):
    if extension == 'json' or extension == 'jsonv2':
        model = data.models_json.get_model_by_extension(extension)
        try:
            json = response.json()
            parse_obj_as(List[model], json)
            error = 0
        except ValidationError as e:
            error = e.errors()
        assert error == 0, f'При валидации ответа произошла ошибка: ' \
                           f'\nactual result = {error}'

    elif extension == 'geojson' or extension == 'geocodejson':
        model = data.models_json.get_model_by_extension(extension)
        try:
            json = response.json()
            model(**json)
            error = 0
        except ValidationError as e:
            error = e.errors()
        assert error == 0, f'При валидации ответа произошла ошибка: ' \
                           f'\nactual result = {error}'

    elif extension == 'xml':
        root = ET.fromstring(response.text)
        assert root.tag in ext.sets.get('xml')['response_search'], f'Тег "{root.tag}" не входит в группу ожидаемых тегов'
        for child in root:
            assert child.tag in ext.sets.get('xml')['response_search'], f'Тег "{child.tag}" не входит в группу ожидаемых тегов'


def connection_response_successful(json):
    model = data.models_json.ConnectionSuccessful
    try:
        model(**json)
        error = 0
    except ValidationError as e:
        error = e.errors()
    assert error == 0, f'При валидации ответа произошла ошибка: ' \
                       f'\nactual result = {error}'


def contents_in_response(extension, response):
    if extension == 'xml' or extension == 'without_format':
        root = ET.fromstring(response.text)
        assert root.tag in ext.sets.get('xml')['fields'], f'Тег "{root.tag}" не входит в группу ожидаемых тегов'
        for child in root:
            assert child.tag in ext.sets.get('xml')['fields'], f'Тег "{child.tag}" не входит в группу ожидаемых тегов'

    elif extension == 'non-existent':
        json = response.json()
        expected_result = ext.get_field_by_extension(extension, 'fields')
        actual_result = json['error']['fields']
        assert expected_result == actual_result, f'Полученный текст ошибки не соответствует ожидаемому:' \
                                                 f'\nexpected result = "{expected_result}",' \
                                                 f'\nactual result = "{actual_result}"'

    else:
        expected_result = ext.get_field_by_extension(extension, 'fields')
        actual_result = response.json()
        assert expected_result in actual_result, f"expected result = '{expected_result}' in '{actual_result}'," \
                                                 f"\nactual result = ожидаемые поля не присутствуют в ответе "
