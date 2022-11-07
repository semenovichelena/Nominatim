from pydantic import BaseModel


class ResponseJSON(BaseModel):
    place_id: int
    licence: str
    osm_type: str
    osm_id: int
    boundingbox: list
    lat: str
    lon: str
    display_name: str


class ResponseJSONV2(BaseModel):
    place_id: int
    licence: str
    osm_type: str
    osm_id: int
    boundingbox: list
    lat: str
    lon: str
    display_name: str


class ResponseGEOJSON(BaseModel):
    type: str
    licence: str
    features: tuple = []


class ResponseGEOCODEJSON(BaseModel):
    type: str
    geocoding: dict
    features: tuple = []


class ConnectionSuccessful(BaseModel):
    status: int = 0
    message: str = 'OK'
    data_updated: str
    software_version: str
    database_version: str


models_response = {
    'json': ResponseJSON,
    'jsonv2': ResponseJSONV2,
    'geojson': ResponseGEOJSON,
    'geocodejson': ResponseGEOCODEJSON
}


def get_model_by_extension(extension):
    for current_model in models_response:
        if current_model == extension:
            return models_response[current_model]
