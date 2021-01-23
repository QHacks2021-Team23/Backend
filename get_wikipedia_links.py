from google.cloud import language_v1
import nltk


# def is_adj(word):
#     '''
#     Checks the part of speech of a word

#     Args:
#         word : word to check
#     Return:
#         True if a word is an adjective

#     '''
#     part_of_speech = nltk.pos_tag(nltk.word_tokenize(word))[0][1]
#     return "J" in part_of_speech

def get_voice(text_content):
    """
    Analyse the voice of the text. Ideal use case for sentence or paragraph.

    Args:
        text_content : The text content to analyze

    Return:
        An array of dictionary that contains the word, and the voice (PASSIVE, ACTIVE, VOICE_UNKNOWN)
    """

    client = language_v1.LanguageServiceClient()


    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}
    encoding_type = language_v1.EncodingType.UTF8


    response = client.analyze_syntax(request = {'document': document, 'encoding_type': encoding_type})
    return_data = []
    # Loop through tokens returned from the API
    for token in response.tokens:
        # Get the text content of this token. Usually a word or punctuation.
        text = token.text
        part_of_speech = token.part_of_speech

        return_data.append(dict(
            text=text.content,
            voice=language_v1.PartOfSpeech.Voice(part_of_speech.voice).name,
        ))
    ##return the voice of the sentence

    return return_data


def get_wikipedia_links(text_content):
    """
    Use NLP to detect interesting people, place or things and provide wikipedia links to them

    Args:
        text_content The text content to analyze

    Return:
        An array of dictionary that has name of phrase, type (PERSON,COMMON,OTHER), and wikipedia url

    """

    client = language_v1.LanguageServiceClient()

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entities(request = {'document': document, 'encoding_type': encoding_type})

    return_data = []

    for entity in response.entities:
        for metadata_name, metadata_value in entity.metadata.items():
            if(metadata_name=='wikipedia_url'):
                return_data.append(dict(
                    name=entity.name,
                    type=language_v1.Entity.Type(entity.type_).name,
                    url=metadata_value
                ))

    return return_data


wikipedia_test = '''
Martin Luther King Jr. (born Michael King Jr.; January 15, 1929 – April 4, 1968) was an American Baptist minister and activist who became the most visible spokesperson and leader in the Civil Rights Movement from 1955 until his assassination in 1968. King is best known for advancing civil rights through nonviolence and civil disobedience, inspired by his Christian beliefs and the nonviolent activism of Mahatma Gandhi. He was the son of early civil rights activist Martin Luther King, Sr..
'''

#passive voice example
passive_voice='''
At dinner, six shrimp were eaten by Harry.
'''

#active voice example
active_voice='''
Harry ate six shrimp at dinner.
'''

#adjective test
adjective_test='''
I love that really big old green antique car that is always parked at the end of the street.
'''

text_content = wikipedia_test
print(get_wikipedia_links(text_content))



# text_content = active_voice
text_content = passive_voice
print(get_voice(text_content))
