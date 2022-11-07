sets = {
    'json': {
        'fields': 'place_id' and 'licence',
        'fields2': 'place_id' and 'licence' and 'osm_type' and 'osm_id' and 'lat' and 'lon' and 'display_name'
                  and 'address' and 'boundingbox',
        'content_type': 'application/json',
        'code': 400,
        'search_fields': ""
    },
    'xml': {
        'fields': ['reversegeocode', 'result', 'addressparts'],
        'content_type': 'text/xml',
        'response_search': ['searchresults', 'place']
    },
    'jsonv2': {
        'fields': 'place_id' and 'licence' and 'osm_type' and 'osm_id' and 'lat' and 'lon' and 'display_name'
                  and 'address' and 'boundingbox',
        'content_type': 'application/json',
    },
    'geojson': {
        'fields': 'type' and 'licence' and 'features',
        'content_type': 'application/json',
    },
    'geocodejson': {
        'fields': 'type' and 'geocoding' and 'features',
        'content_type': 'application/json',
    },
    'non-existent': {
        'fields': 'error',
        'content_type': 'application/json',
        'code': 400,
        'message': "Parameter 'format' must be one of: xml, json, jsonv2, geojson, geocodejson"
    },
    'without_format': {
        'fields': ['reversegeocode', 'result', 'addressparts'],
        'content_type': 'text/xml',
    },
    'text': {
        'content_type': 'text/html',
    }
}


def get_field_by_extension(extension, field_name):
    for current_set in sets:
        if current_set == extension:
            return sets[current_set][field_name]
