import json
from PyDictionary import PyDictionary
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import language_tool_python
import string
# import get_wikipedia_links as app
import random
from flask import Flask, jsonify,request
from google.cloud import language_v1

app = Flask(__name__)

setting = "en-CA"


    #tense,
def countWords(words):
  dictCount = {}
  stopword = set(stopwords.words('english'))

  words = words.translate(str.maketrans('', '', string.punctuation))
  word_tokens = word_tokenize(words)
  arrayWords = []

  for i in word_tokens:

    if i.lower() not in stopword:

          arrayWords.append(i.lower())


  for j in arrayWords:

    if j in dictCount.keys():

          dictCount[j] = dictCount[j] + 1

    else:
          dictCount[j] = 1


  return dictCount


def replaceWord(sentence, wordToReplace):

  dictionary=PyDictionary()

  words = word_tokenize(sentence)

  newSentence = ""

  for word in words:
    newWord = word
    if (word == wordToReplace):


      newWordArray = dictionary.synonym(wordToReplace)
      newWord = random.choices(newWordArray)
    newSentence = newSentence + " " + newWord

  return newSentence



def get_voice(text_content):
    # print("getting voice")
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

    # print("Get Voice returned successfully...")

    for dictionary in return_data:
        if dictionary["voice"] == "PASSIVE":
            return "PASSIVE"
    return "ACTIVE"
    ##return the voice of the sentence

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
                    url=metadata_value
                ))
    # print("Get Wiki Links returned successfully...")
    return return_data


def parseData(data):

  print(json.load(data))

  # print("parsedata")
  # text - string
  # array of paragraphs
  #
  # return a text

  # essay = json.load(data)
  #make it look
  # essay = json.load(data)[array]

  # essay = ['''
  # Looking back on a childhood filled with events and memories, I find it rather difficult to pick one that leaves me with the fabled "warm and fuzzy feelings." As the daughter of an Air Force major, I had the pleasure of traveling across America in many moving trips. I have visited the monstrous trees of the Sequoia National Forest, stood on the edge of the Grand Canyon and have jumped on the beds at Caesar's Palace in Lake Tahoe. The day I picked my dog up from the pound was one of the happiest days of both of our lives. I had gone to the pound just a week earlier with the idea that I would just "look" at a puppy. Of course, you can no more just look at those squiggling little faces so filled with hope and joy than you can stop the sun from setting in the evening. I knew within minutes of walking in the door that I would get a puppy… but it wasn't until I saw him that I knew I had found my puppy. Looking for houses was supposed to be a fun and exciting process. Unfortunately, none of the ones that we saw seemed to match the specifications that we had established. They were too small, too impersonal, too close to the neighbors. After days of finding nothing even close, we began to wonder: was there really a perfect house out there for us?
  # ''',
  # '''
  # The afternoon grew so glowering that in the sixth inning the arc lights were turned on--always a wan sight in the daytime, like the burning headlights of a funeral procession. Aided by the gloom, Fisher was slicing through the Sox rookies, and Williams did not come to bat in the seventh. He was second up in the eighth. This was almost certainly his last time to come to the plate in Fenway Park, and instead of merely cheering, as we had at his three previous appearances, we stood, all of us, and applauded
  # ''']

  # essay = data

  # essayAsArray = []

  # tool = language_tool_python.LanguageTool(setting)

  # for para in essay:
  #   sentences = para.re.split('.|!|?', str)
  #   sentenceChangedDict = {}
  #   wikipediaArr = {}
  #   sentenceChangedArray = []
  #   paragraphsWordCount = {}

  #   sentences = [x for x in sentences if x] #get rid of null

  #   paragraph = ""

  #   for sentence in sentences:

  #     newString = sentence

  #     if(sentence != tool.correct(sentence)):
  #       newString = tool.correct(sentence)

  #     sentenceWordCount = countWords(newString)

  #     paragraphWordCount = mergeDictionary(paragraphWordCount, sentenceWordCount)

  #     ##uncomment later
  #     print('getting voice')
  #     voice = get_voice(newString)
  #     print('getting links')
  #     wikipediaArr = get_wikipedia_links(newString)

  #     sentenceChangedDict["changed"] = newString != sentence
  #     sentenceChangedDict["sentence"] = newString
  #     sentenceChangedDict["voice"] = voice

  #     sentenceChangedArray.append(sentenceChangedArray)      

  #   if len(wikipediaArr) == 0: wikipediaArr[0] = {"name" : False}

  #   paragraph = {"sentencesArray" : sentenceChangedArray, "wikipediaArray" : wikipediaArr, "occurance" : paragraphWordCount}
  #   essayAsArray.append(paragraph)

  # print('returning data')
  # print(essayAsArray)
  # return essayAsArray
  return 0


@app.route('/', methods=['GET','POST']) 
def home():
  arrayOfParagraphs = request.get_json()["data"] #accept json, key data, and value as an array of strings
  print(arrayOfParagraphs)
  if arrayOfParagraphs:
    data = parseData(arrayOfParagraphs)
    return jsonify(data)
  else:
    return "no data was given"

@app.route('/changeLanguage',methods=['POST'])
def change():
  setting = request.data.decode("utf-8")


if __name__ == '__main__':
    app.run(debug=True)
