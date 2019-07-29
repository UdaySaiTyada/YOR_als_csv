import nltk
import gensim
from nltk.corpus import abc

a = 1
print("Model is training")
model= gensim.models.Word2Vec(abc.sents())
print("1")
X= list(model.wv.vocab)
print("2")
data=model.most_similar('science')
print("3")
print(data)
print("Training Completed")
