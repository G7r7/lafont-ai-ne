#!/usr/bin/env python3

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import TextVectorization
import keras_nlp
import numpy as np

import random
from pathlib import Path

from dataset import (
    vocab_size,
    text_valid,
    train_dataset,
    test_dataset,
    valid_dataset,
    index_lookup,
    vectorizer,
    seq_length
)

APP_DIR = Path.home() / ".lafontaine"
DATASET = APP_DIR / "dataset.txt"
VECTORIZER = APP_DIR / "vectorizer.pkl"

# seq_length = 50
embed_dim = 128
num_heads = 4


def create_model():
    inputs = keras.layers.Input(shape=(None,), dtype=tf.int32, ragged=True)
    embedding_layer = keras_nlp.layers.TokenAndPositionEmbedding(vocabulary_size=vocab_size, 
                                                     sequence_length=seq_length, 
                                                     embedding_dim=embed_dim)(inputs)
    decoder = keras_nlp.layers.TransformerDecoder(intermediate_dim=embed_dim, 
                                                            num_heads=num_heads, 
                                                            dropout=0.5)(embedding_layer)
    
    outputs = keras.layers.Dense(vocab_size, activation='softmax')(decoder)
    
    model = keras.Model(inputs=inputs, outputs=outputs)
    
    model.compile(
        optimizer="adam", 
        loss='sparse_categorical_crossentropy',
        metrics=[keras_nlp.metrics.Perplexity(), 'accuracy']
    )
    return model

model = create_model()
model.summary()

class TextSampler(keras.callbacks.Callback):
    def __init__(self, start_prompt, max_tokens):
        self.start_prompt = start_prompt
        self.max_tokens = max_tokens
        
    # Helper method to choose a word from the top K probable words with respect to their probabilities
    # in a sequence
    def sample_token(self, logits):
        logits, indices = tf.math.top_k(logits, k=5, sorted=True)
        indices = np.asarray(indices).astype("int32")
        preds = keras.activations.softmax(tf.expand_dims(logits, 0))[0]
        preds = np.asarray(preds).astype("float32")
        return np.random.choice(indices, p=preds)

    def on_epoch_end(self, epoch, logs=None):
        decoded_sample = self.start_prompt
        
        for i in range(self.max_tokens-1):
            tokenized_prompt = vectorizer([decoded_sample])[:, :-1]
            predictions = self.model.predict([tokenized_prompt], verbose=0)
            # To find the index of the next word in the prediction array.
            # The tokenized prompt is already shorter than the original decoded sample
            # by one, len(decoded_sample.split()) is two words ahead - so we remove 1 to get
            # the next word in the sequence
            sample_index = len(decoded_sample.strip().split())-1
            
            sampled_token = self.sample_token(predictions[0][sample_index])
            sampled_token = index_lookup[sampled_token]
            decoded_sample += " " + sampled_token
            
        print(f"\nSample text:\n{decoded_sample}...\n")

# First 5 words of a random sentence to be used as a seed
random_sentence = ' '.join(random.choice(text_valid).replace('\n', ' ').split(' ')[:4])
sampler = TextSampler(random_sentence, 30)
reducelr = keras.callbacks.ReduceLROnPlateau(patience=10, monitor='val_loss')