from importlib import import_module
from PyDictionary import PyDictionary
from dotenv import load_dotenv
import os
load_dotenv()
FRONTEND_URL = os.getenv('FRONTEND_URL')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import language_tool_python
import string
import re
# import get_wikipedia_links as app
import random
from flask import Flask, jsonify, request, json
from flask_cors import CORS
api = import_module('api')

# from google.cloud import language_v1

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

setting = "en-CA"

# tense,


def mergeDictionary(d1, d2):

    d = {}
    for k in d1.keys():
        d[k] = d1[k]
        if(k in d2):
            d[k] = d[k] + d2[k]
    for k in d2.keys():
        if k not in d1:
            d[k] = d2[k]

    return d


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


# def replaceWord(sentence, wordToReplace):

#     dictionary = PyDictionary()

#     words = word_tokenize(sentence)

#     newSentence = ""

#     for word in words:
#         newWord = word
#         if (word == wordToReplace):

#             newWordArray = dictionary.synonym(wordToReplace)
#             newWord = random.choices(newWordArray)
#         newSentence = newSentence + " " + newWord

#     return newSentence


def parseData(data):

    paragraphs = data

    essayAsArray = []

    tool = language_tool_python.LanguageTool(setting)

    for para in paragraphs:

        sentences = re.split('([^!|?|.]*[!|?|.])', para)

        sentenceChangedDict = {}
        wikipediaArr = []
        sentenceChangedArray = []
        paragraphWordCount = {}

        sentences = [x for x in sentences if x]  # get rid of null

        paragraph = ""

        i = 0

        for sentence in sentences:

            i += 1

            if (len(''.join(sentence.split(' '))) == 0):
                continue

            newString = sentence

            if(sentence != tool.correct(sentence)):
                newString = tool.correct(sentence)

            sentenceWordCount = countWords(newString)

            paragraphWordCount = mergeDictionary(
                paragraphWordCount, sentenceWordCount)

            voice = api.get_voice_api(newString)
            wikis = api.get_wiki_api(newString)

            sentenceChangedDict["changed"] = newString != sentence
            sentenceChangedDict["sentence"] = newString
            sentenceChangedDict["voice"] = voice
            sentenceChangedDict["wikis"] = wikis
            sentenceChangedArray.append(dict(sentenceChangedDict))

        paragraph = {"sentencesArray": list(sentenceChangedArray),
                     "occurrence": dict(paragraphWordCount), "sentenceCount": i}

        essayAsArray.append(dict(paragraph))

    return essayAsArray


def getSynonym(wordToReplace):

    dictionary = PyDictionary()

    return dictionary.synonym(wordToReplace)


@app.route('/', methods=['POST'])
def home():
    # accept json, key data, and value as an array of strings
    data = parseData(request.get_json(force=True))
    print(data)
    return jsonify(data)


# @app.route('/changeLanguage', methods=['POST'])
# def change():
#     setting = request.data.decode("utf-8")


@app.route('/getSynonym', methods=['POST'])
def syn():
    data = request.get_json(force=True)
    synonyms = getSynonym(data)
    if (len(synonyms) != 0):
        return jsonify(synonyms)
    else:
        return {"error": True}


if __name__ == '__main__':
    #sentences = para.split(r'.|!|\?')

    para = 'Hello. My name is Jeff! What are you doing? Hello ?'

    print(re.split('(\s[^!|?|\.]*[!|?|\.])', para))

    app.run(debug=False, host='0.0.0.0', port='5000')
