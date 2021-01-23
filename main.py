import json
from PyDictionary import PyDictionary
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize 
import string

def mergeDictionary(d1, d2):
  d = {}
  for k in d1.keys():
    d[k] = tuple(d[k] for d in ds)

  return d

def countWords(words):
  dictCount = {}; 
  stopwords = set(stopwords.words('english'))

      
  word_tokens = word_tokenize(words)
  arrayWords = []

  for i in word_tokens: 
    
    if i not in stopwords:
          
          arrayWords.append(i)
          

  for j in arrayWords:
        
    if j in dictCount.keys():
          
          dictCount[j] = dictCount[j] + 1

    else:
          dictCount[j] = 1


  return dictCount
      
def replaceCharacter(s, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]

def checkPunctuation(words):
    #search each character for puntuation using a for loop in range length of string
    for i in range(len(words)):
      quoteCount = 0
          #check if its a punctuation character
      if words[i] == '"':
        quoteCount += 1
        break
      elif(words[i] in string.punctuation):
            if words[i-1] == ' ':
              words = replaceCharacter(words, '', i) #check i-1 if its space there is a problem      

      if (words[i] == '"' and words[i]-1 == '.'):

        if (quoteCount%2 == 0):
          words = replaceCharacter(words, ' "', i)
        else:
          words = replaceCharacter(words, '".', i-1)

      if(words[i] in string.punctuation):

        if((words[i-1] == '.' and words[i+1] == '.') or (words[i-1] == '.' and words[i-2] == '.')) continue
        
        if(words[i-1] in string.punctuation and words[i-1] != '"' and words[i-1] != ")"):
          #TODO: Figure out punctuation which one takes priority and which one i remove

      
      if(quoteCount%2 == 1):
        #TODO: Write code saying either too little or too many quotation marks
                      


def main(data):
  essay = json.load(data)

  essayWordCount = {}

  essayAsString = ""

  for i in essay.keys("Sentences"):
    
    sentenceWordCount = countWords(i)

    essayWordCount = mergeDictionary(essayWordCount, sentenceWordCount)

    essayAsString = essayAsString + i

    #wait for api function call it here on each sentence

  #essayParagraphs = essayAsString.split("\n")

  #essayAsString = ""

  #for paragraphs in essayParagraphs:wq
    
    #essayAsString = essayAsString + paragraphs

def replaceWord(sentence, wordToReplace):
  
  dictionary=PyDictionary()

  words = word_tokenize(sentence)

  newSentence = ""

  for i in range(len(words)):

    if (words[i] == wordToReplace):
          
      words[i] = dictionary.synonym(wordToReplace)
    
    newSentence = newSentence + " " + words[i]