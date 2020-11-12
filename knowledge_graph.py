import pandas as pd

import spacy
from spacy import displacy
from spacy.matcher import Matcher
from spacy.tokens import Span

import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(nlp.create_pipe("sentencizer"))

dataset = pd.read_csv("scraped_articles.csv",
                      sep="[ \t]*,[ \t]*", engine="python")

print(dataset.shape)

def clean_text(text):
    text = " ".join(text.split())
    text = text.replace("“", "")
    text = text.replace("”", "")
    return text

def get_sentences(text):
    document = nlp(text)
    return [sent.string.strip() for sent in document.sents]


text = dataset["post"][0]
# print(text)


# total_sentences = 0
sentences = get_sentences(clean_text(text))
# for s in sentences:
#     total_sentences += 1
#     print(s)
#     print("     ---     ")

# print("total sentences ", total_sentences)
print(sentences[1])
doc = nlp(sentences[1])
for tok in doc:
    print(tok.text, "...", tok.dep_)