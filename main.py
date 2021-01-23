import json
from PyDictionary import PyDictionary
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import language_tool_python
import string
import get_wikipedia_links as app
import random
import re

def mergeDictionary(d1, d2):
  d = {}
  for k in d1.keys():
    d[k] = tuple(d[k] for d in ds)

  return d

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


def parseData(data):
  # text - string
  # array of paragraphs
  #
  # return a text

  essay = json.load(data)
  #make it look
  # essay = json.load(data)[array]

  print(essay)

  essay = data

  essayAsArray = []

  tool = language_tool_python.LanguageTool('en-CA')


  for para in essay:
    sentences = para.re.split('.|!|?', str)
    sentenceChangedDict = {}
    wikipediaArr = {}
    sentenceChangedArray = []
    paragraphsWordCount = {}

    paragraph = ""

    for sentence in sentences:

      newString = sentence

      if(sentence != tool.correct(sentence)):
        newString = tool.correct(sentence)

      sentenceWordCount = countWords(newString)

      paragraphWordCount = mergeDictionary(paragraphWordCount, sentenceWordCount)

      ##uncomment later
      voice = "ACTIVE"
      # voice = app.get_voice(newString)
      
      # wikipediaArr = app.get_wikipedia_links(newString)
      # # wikipediaArr = [{"name":"WORD","url":"https://wikipedia.org"}]

      sentenceChangedDict["changed"] = newString != sentence
      sentenceChangedDict["sentence"] = newString
      sentenceChangedDict["voice"] = voice

      sentenceChangedArray.append(sentenceChangedArray)      

    if len(wikipediaArr) == 0: wikipediaArr[0] = {"name" : False}

    paragraph = {"sentencesArray" : sentenceChangedArray, "wikipediaArray" : wikipediaArr, "occurance" : paragraphWordCount}
    essayAsArray.append(paragraph)

    #essayAsArray formatted as Array of Dictionaries of Array of Dictionaries

  return essayAsArray

def getSynonym(wordToReplace):

  dictionary=PyDictionary()     

  return dictionary.synonym(wordToReplace)