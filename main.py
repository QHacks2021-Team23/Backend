import json
from PyDictionary import PyDictionary
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import language_tool_python
import string
import get_wikipedia_links as app
import random

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

  # essay = json.load(data)
  #make it look
  # essay = json.load(data)[array]

  # essay = ['''
  # Looking back on a childhood filled with events and memories, I find it rather difficult to pick one that leaves me with the fabled "warm and fuzzy feelings." As the daughter of an Air Force major, I had the pleasure of traveling across America in many moving trips. I have visited the monstrous trees of the Sequoia National Forest, stood on the edge of the Grand Canyon and have jumped on the beds at Caesar's Palace in Lake Tahoe. The day I picked my dog up from the pound was one of the happiest days of both of our lives. I had gone to the pound just a week earlier with the idea that I would just "look" at a puppy. Of course, you can no more just look at those squiggling little faces so filled with hope and joy than you can stop the sun from setting in the evening. I knew within minutes of walking in the door that I would get a puppy… but it wasn't until I saw him that I knew I had found my puppy. Looking for houses was supposed to be a fun and exciting process. Unfortunately, none of the ones that we saw seemed to match the specifications that we had established. They were too small, too impersonal, too close to the neighbors. After days of finding nothing even close, we began to wonder: was there really a perfect house out there for us?
  # ''',
  # '''
  # The afternoon grew so glowering that in the sixth inning the arc lights were turned on--always a wan sight in the daytime, like the burning headlights of a funeral procession. Aided by the gloom, Fisher was slicing through the Sox rookies, and Williams did not come to bat in the seventh. He was second up in the eighth. This was almost certainly his last time to come to the plate in Fenway Park, and instead of merely cheering, as we had at his three previous appearances, we stood, all of us, and applauded
  # ''']

  essay = data
  #split sentences

  #essayWordCount = {}

  #essayAsString = ""

  essayAsArray = []

  tool = language_tool_python.LanguageTool('en-CA')


  for para in essay:
    sentences = para.split(".")
    sentenceChangedDict = {}
    wikipediaArr = {}
    sentenceChangedArray = []

    for sentence in sentences:

      newString = sentence

      if(sentence != tool.correct(sentence)):
        newString = tool.correct(sentence)

      sentenceWordCount = countWords(newString)

      for word in sentenceWordCount:  #check if a word appears too many times
        if (sentenceWordCount[word] >= 3):
          newString = replaceWord(newString, word)
      
      if(sentence != tool.correct(sentence)):
        newString = tool.correct(newString)
      ## wikipedia link
      ## voice

      # [{
      #   sentence: {info},
      #   sentence: {info},
      #   sentence: {info}
      # },
      # {
      #   sentence: (Bool,String,Arr)
      # }]

      ##uncomment later
      voice = app.get_voice(newString)
      
      wikipediaArr = app.get_wikipedia_links(newString)
      # voice = "PASSIVE"
      # wikipediaArr = [{"name":"WORD","url":"https://wikipedia.org"}]

      if (newString != sentence):
        sentenceChangedDict[newString] = (True, voice)
      else:
        sentenceChangedDict[newString] = (False, voice)


    sentenceChangedArray.append(sentenceChangedDict)


    paragraph = [sentenceChangedArray, wikipediaArr]
    essayAsArray.append(paragraph)

  print(essayAsArray)

    #Array of Arrays of Array of Dictionaries

    #wait for api function call it here on each sentence

  #essayParagraphs = essayAsString.split("\n")

  #essayAsString = ""

  #for paragraphs in essayParagraphs:wq

    #essayAsString = essayAsString + paragraphs

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



essay = ['''
  Looking back on a childhood filled with events and memories, I find it rather difficult to pick one that leaves me with the fabled "warm and fuzzy feelings." 
  As the daughter of an Air Force major, I had the pleasure of traveling across America in many moving trips. 
  I have visited the monstrous trees of the Sequoia National Forest, stood on the edge of the Grand Canyon and have jumped on the beds at Caesar's Palace in Lake Tahoe. 
  The day I picked my dog up from the pound was one of the happiest days of both of our lives. 
  I had gone to the pound just a week earlier with the idea that I would just "look" at a puppy. Of course, you can no more just look at those squiggling little faces so filled with hope and joy than you can stop the sun from setting in the evening. I knew within minutes of walking in the door that I would get a puppy… but it wasn't until I saw him that I knew I had found my puppy. Looking for houses was supposed to be a fun and exciting process. Unfortunately, none of the ones that we saw seemed to match the specifications that we had established. They were too small, too impersonal, too close to the neighbors. After days of finding nothing even close, we began to wonder: was there really a perfect house out there for us?
  ''',
  '''
  The afternoon grew so glowering that in the sixth inning the arc lights were turned on--always a wan sight in the daytime, like the burning headlights of a funeral procession. Aided by the gloom, Fisher was slicing through the Sox rookies, and Williams did not come to bat in the seventh. He was second up in the eighth. This was almost certainly his last time to come to the plate in Fenway Park, and instead of merely cheering, as we had at his three previous appearances, we stood, all of us, and applauded
  ''']
parseData(essay)