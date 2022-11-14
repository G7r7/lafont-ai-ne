#!/usr/bin/env python3

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import TextVectorization
import keras_nlp
import numpy as np
import pickle

import random
from pathlib import Path

APP_DIR = Path.home() / ".lafontaine"
DATASET = APP_DIR / "dataset.txt"
VECTORIZER = APP_DIR / "vectorizer.pkl"

with VECTORIZER.open('rb') as stream:
    from_disk = pickle.load(stream)

vectorizer = TextVectorization.from_config(from_disk['config'])
vectorizer.set_weights(from_disk['weights'])

seq_length = from_disk['seq_length']

with DATASET.open('r') as stream:
    verses = stream.read().splitlines()

print(max(verses, key=lambda v: len(v.split())))

random.shuffle(verses)
length = len(verses)
text_train = verses[:int(0.7*length)]
text_test = verses[int(0.7*length):int(0.85*length)]
text_valid = verses[int(0.85*length):]

batch_size = 64

train_dataset = tf.data.Dataset.from_tensor_slices(text_train)
train_dataset = train_dataset.shuffle(buffer_size=256)
train_dataset = train_dataset.batch(batch_size)

test_dataset = tf.data.Dataset.from_tensor_slices(text_test)
test_dataset = test_dataset.shuffle(buffer_size=256)
test_dataset = test_dataset.batch(batch_size)

valid_dataset = tf.data.Dataset.from_tensor_slices(text_valid)
valid_dataset = valid_dataset.shuffle(buffer_size=256)
valid_dataset = valid_dataset.batch(batch_size)

def preprocess_text(text):
    text = tf.expand_dims(text, -1)
    tokenized_sentences = vectorizer(text)
    x = tokenized_sentences[:, :-1]
    y = tokenized_sentences[:, 1:]
    return x, y

train_dataset = train_dataset.map(preprocess_text)
train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)

test_dataset = test_dataset.map(preprocess_text)
test_dataset = test_dataset.prefetch(tf.data.AUTOTUNE)

valid_dataset = valid_dataset.map(preprocess_text)
valid_dataset = valid_dataset.prefetch(tf.data.AUTOTUNE)

vocab = vectorizer.get_vocabulary()
vocab_size = len(vocab)
index_lookup = dict(zip(range(len(vocab)), vocab))