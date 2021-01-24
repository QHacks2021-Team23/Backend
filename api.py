import requests
from dotenv import load_dotenv
import os
load_dotenv()
SECRET_KEY = os.getenv('GOOGLE_API_KEY')


def get_wiki_api(text_content):
    body = {
    "document":{
        "type":"PLAIN_TEXT",
        "language": "EN",
        "content": text_content
    },
    "encodingType":"UTF8"
    }
    res = requests.post('https://language.googleapis.com/v1/documents:analyzeEntities?key='+SECRET_KEY, json=body)
    res = res.json()
    return_data = []

    for entity in res['entities']:
        for metadata_name, metadata_value in entity['metadata'].items():
            if(metadata_name=='wikipedia_url'):
                return_data.append(dict(
                    name=entity['name'],
                    url=metadata_value
                ))
    return return_data





# wikipedia_test = '''Martin Luther King Jr. (born Michael King Jr.; January 15, 1929 – April 4, 1968) was an American Baptist minister and activist who became the most visible spokesperson and leader in the Civil Rights Movement from 1955 until his assassination in 1968. King is best known for advancing civil rights through nonviolence and civil disobedience, inspired by his Christian beliefs and the nonviolent activism of Mahatma Gandhi. He was the son of early civil rights activist Martin Luther King, Sr..'''

# print(get_wiki_api(wikipedia_test))















