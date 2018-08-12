"""
Embeddings
by D. Hakkani-Tur
"""


import re
import numpy as np

"""
class InputVec(object):
	def __init__(self, input_data, encode_type, embeddingFile=None):
		num_sample, time_length = np.shape(input_data)
		if encode_type == '1hot':
			self.encoding = np.zeros((num_sample, time_length, ))
			for i, sent in enumerate(input_tensor):
				for j, k in enumerate(sent):
					self.encoding[i][j][k] = 1
#		elif encode_type == 'embedding':
		elif encode_type == 'pretrained' and embeddingFile != None:
			self.inputvec = readEmbeddings(embeddingFile)

	def getEmbeddingDim(self):
		if encode_type == '1hot':
		elif encode_type == 'pretrained':
			return self.inputvec['embeddingSize']
"""

class PredefinedEmbedding(object):
   """
     dictionary of embeddings
   """

   def __init__(self,embeddingFile):
       
       self.embeddings = readEmbeddings(embeddingFile)

   def getEmbeddingDim(self):
     return self.embeddings['embeddingSize']

   def getWordEmbedding(self,word):
       if word == "BOS":
           return self.embeddings['embeddings']["</s>"]
       elif word == "EOS":
           return self.embeddings['embeddings']["</s>"]
       elif word in self.embeddings['embeddings']:
           return self.embeddings['embeddings'][word]
       else:
           return np.zeros((self.embeddings['embeddingSize'],1))


def readEmbeddings(embeddingFile):

# read the word embeddings
# each line has one word and a vector of embeddings listed as a sequence of real valued numbers

  wordEmbeddings = {}
  first = True
  p=re.compile('\s+')

  for line in open(embeddingFile, 'r'):
     d=p.split(line.strip())
     if (first):
         first = False
         size = len(d) -1
     else:
         if (size != len(d) -1):
             print("Problem with embedding file, not all vectors are the same length\n")
             exit()
     currentWord = d[0]
     wordEmbeddings[currentWord] = np.zeros((size,1))
     for i in range(1,len(d)):
         wordEmbeddings[currentWord][i-1] = float(d[i])
  embeddings={'embeddings':wordEmbeddings, 'embeddingSize': size}
  return embeddings
