import requests
def main_encode(json_data):

    detail_value = []
    try:
        l = next((i, d) for i, d in enumerate(json_data) if ('label' in d) and (d['label'] != None))
        name = ''.join(l[1]['label'])
    except:
        name = ''
    try:
        l = next((i, d) for i, d in enumerate(json_data) if ('description' in d) and (d['description'] != None))
        description = ''.join(l[1]['description'])
    except:
        description = ''
    try:
        l = next((i, d) for i, d in enumerate(json_data) if ('synonyms' in d) and (d['synonyms'] != None))
        synonyms = ''.join(l[1]['synonyms'])
    except:
        synonyms = ''
    try:
        l = next((i, d) for i, d in enumerate(json_data) if
                 ('database_cross_reference' in d['annotation']) and (d['description'] != None))
        dbscr = '*'.join(l[1]['annotation']['database_cross_reference'])
    except:
        dbscr = ''

    name = name
    description = description
    synonyms = synonyms
    data_base_cross_reference = dbscr
    detail_value.extend([name,description,synonyms,data_base_cross_reference])

    return detail_value