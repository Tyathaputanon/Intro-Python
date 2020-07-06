# -*- coding: utf-8 -*-
"""INFO490-FindingCharacters

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TAHVB7Jf3__HLdU2HkGFJXICmt_5HAsK
"""

import collections 
from collections import Counter 
import requests
import re

#
# already done
# 

def normalize_token(token):
  return token.strip().strip("'")
  
def read_remote(url):
  import requests
  with requests.get(url) as response:
    response.encoding = 'utf-8'
    return response.text
  return None

def load_stop_words():
  return ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']
 
# 
# use your code
#

def split_text_into_tokens(text):
  # regex = '[\'A-Za-z0-9]+-?[\'A-Za-z0-9]+'
  # find = re.compile(regex)  #2
  # keywords = find.findall(text)     #3
  # return [normalize_token(keyword) for keyword in keywords]
  pattern = r"['A-Za-z0-9]+-?['A-Za-z0-9]+"
  regex = re.compile(pattern, re.IGNORECASE)
  tokens = regex.findall(text)
  tokens = [i.strip("'") for i in tokens]
  return tokens
  
def bi_grams(tokens):
  # return [(tokens[i-1], tokens[i]) for i in range(1,len(tokens))]
  bigrams = []
  for idx, i in enumerate(tokens):
    if idx == (len(tokens)-1):
      break
    else:
      bigrams.append((tokens[idx],tokens[idx+1]))
  return bigrams 

def top_n(tokens, n):
  tokenCounter = collections.Counter()
  for token in tokens:
    tokenCounter[token] += 1
  return (tokenCounter.most_common(n))

def remove_stop_words(tokens, stoplist):
  stop_words = [stop_word.lower() for stop_word in stoplist]
  output = []
  for token in tokens:
    if (token.lower() in stop_words):
      pass
    else:
      output.append(token)
  return output 

#
# NEW 
#

def get_titles(text):
  #print (text)
  text = normalize_token(text)
  regexPattern1 = '[A-Z][a-z]{1,3}\.'
  regexPat1   = re.compile(regexPattern1)  #2
  title_tokens = regexPat1.findall(text)     #3
  title_tokensFin = [sub[:-1] for sub in title_tokens]
  #print (title_tokens)
  regexPattern2 = '[A-Z][a-z]{1,3}\s'
  regexPat2   = re.compile(regexPattern2)  #2
  psuedo_titles = regexPat2.findall(text)
  pseudo_titlesFin = [sub[:-1] for sub in psuedo_titles]
  titles = (list)((set)(title_tokensFin)-(set)(pseudo_titlesFin))
  return titles
  
def find_characters_v1(text, stoplist, top):
  tokens = split_text_into_tokens(text)
  tokens = remove_stop_words(tokens, stoplist)
  tokens = [token for token in tokens if token[0].isupper()]
  tokens = top_n(tokens, 15)
  return tokens 

def find_characters_v2(text, stoplist, top):
  lower_stoplist = [stop_word.lower() for stop_word in stoplist]
  tokens = split_text_into_tokens(text)
  tokens = bi_grams(tokens)
  tokens = [token for token in tokens if token[0][0].isupper() and token[1][0].isupper() and token[0].lower() not in lower_stoplist and token[1].lower() not in lower_stoplist]
  tokens = top_n(tokens, 15)
  return tokens
  
def find_characters_v3(text, stoplist, top):
  lower_stoplist = [stop_word.lower() for stop_word in stoplist]
  titles = get_titles(text)
  tokens = split_text_into_tokens(text)
  tokens = bi_grams(tokens)
  tokens = [token for token in tokens if token[0] in titles and token[1][0].isupper() and token[1].lower() not in lower_stoplist]
  tokens = top_n(tokens, 15)
  return tokens  

### Testing Code ###

HUCK_URL= "https://raw.githubusercontent.com/NSF-EC/INFO490Assets/master/src/datasets/pg/huckfinn/huck.txt"
text = read_remote(HUCK_URL)
stop = load_stop_words()

def demo_test():
  text = read_remote(HUCK_URL)
  stop = load_stop_words()
  tokens  = split_text_into_tokens(text)
  cleaned = remove_stop_words(tokens, stop)

  grams = bi_grams(cleaned)
  print(top_n(grams, 10))

#demo_test() 


v1  = find_characters_v1(text, stop, 15)
#print(v1)
v2  = find_characters_v2(text, [], 15)
#print(v2)
titles = get_titles(text)
#print(titles)
v3  = find_characters_v3(text, stop, 15)
#print(v3)