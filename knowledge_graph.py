from typing import Match
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

print("Dataset loaded.")


def clean_text(text):
    text = " ".join(text.split())
    text = text.replace("“", "")
    text = text.replace("”", "")
    return text


def get_sentences(text):
    document = nlp(text)
    return [sent.string.strip() for sent in document.sents]


def get_entities(sent):
    ent1 = ""
    ent2 = ""

    prev_tok_dep = ""
    prev_tok_text = ""

    prefix = ""
    modifier = ""

    for tok in nlp(sent):
        # If token is a punctuation mark, move on to next token
        if tok.dep_ != "punct":
            # Check if token is a compound word
            if tok.dep_ == "compound":
                prefix = tok.text
                # If prev word was also 'compound', add current word to it
                if prev_tok_dep == "compound":
                    prefix = prev_tok_text + " " + tok.text

            # Check if token is modifier
            if tok.dep_.endswith("mod") == True:
                modifier = tok.text
                # If prev word was also 'compound', add current word to it
                if prev_tok_dep == "compound":
                    modifier = prev_tok_text + " " + tok.text

            if tok.dep_.find("subj") == True:
                ent1 = modifier + " " + prefix + " " + tok.text
                prefix = ""
                modifier = ""
                prev_tok_dep = ""
                prev_tok_text = ""

            if tok.dep_.find("obj") == True:
                ent2 = modifier + " " + prefix + " " + tok.text

            # Update variables
            prev_tok_dep = tok.dep_
            prev_tok_text = tok.text

    return [ent1.strip(), ent2.strip()]


def get_relations(sent):
    doc = nlp(sent)

    # Matcher class object
    matcher = Matcher(nlp.vocab)

    # Pattern define
    pattern = [{"DEP": "ROOT"},
               {"DEP": "prep", "OP": "?"},
               {"DEP": "agent", "OP": "?"},
               {"POS": "ADJ", "OP": "?"}]

    matcher.add("matching_1", None, pattern)
    matches = matcher(doc)
    k = len(matches) - 1

    span = doc[matches[k][1]:matches[k][2]]

    return (span.text)









print("Total number of articles: {}\n".format(dataset.shape[0]))

sentence_list = []
print("Extracting individual sentences from every articles...")
for data in tqdm(dataset["post"]):
    sentences = get_sentences(clean_text(data))
    for sentence in sentences:
        sentence_list.append(sentence)

print("Total number of sentences: {}\n".format(len(sentence_list)))

entity_pairs = []

print("Extracting subject-object entity pairs from sentences...")
for s in tqdm(sentence_list):
    entity_pairs.append(get_entities(s))

relations = []
print("\nExtracting relations from sentences...")
for s in tqdm(sentence_list):
    relations.append(get_relations(s))

