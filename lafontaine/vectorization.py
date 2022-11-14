#!/usr/bin/env python3

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import TextVectorization
import tensorflow_text as tf_text
import keras_nlp
import numpy as np
import pickle

import random
from pathlib import Path

APP_DIR = Path.home() / ".lafontaine"
DATASET = APP_DIR / "dataset.txt"
VECTORIZER = APP_DIR / "vectorizer.pkl"

with DATASET.open('r') as stream:
    verses = stream.read().splitlines()

# seq_length = len(max(verses, key=lambda v: len(v.split())))
seq_length = 50

def nw_split(text_input):
    splitted = tf_text.regex_split(input=text_input,
            delim_regex_pattern="[^\w\s]+|\s+",
            keep_delim_regex_pattern="\S+"
            )
    return splitted

vectorizer = TextVectorization(
    split=nw_split,
    standardize='lower',
    output_mode="int",
    output_sequence_length=seq_length + 1,
)

vectorizer.adapt(verses)
# vocab = vectorizer.get_vocabulary()
# vocab_size = len(vocab)

with VECTORIZER.open('wb') as stream:
    pickle.dump(
        {
            'config': vectorizer.get_config(),
            'weights': vectorizer.get_weights(),
            'seq_length': seq_length
        }, 
        stream
    )

# print(verses[42])
# print(vectorizer(verses[42]))
