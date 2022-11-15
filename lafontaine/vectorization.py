import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import TextVectorization
import tensorflow_text as tf_text
import keras_nlp
import numpy as np
import pickle
import random
from pathlib import Path

def nw_split(text_input):
    splitted = tf_text.regex_split(input=text_input,
            delim_regex_pattern="[^\[a-zA-ZÀ-ÿœ']+|\s+", # We split on french words and punctuations
            keep_delim_regex_pattern="[a-zA-ZÀ-ÿœ']" # We keep everything that isn't a sequence of whitespaces
            )
    return splitted