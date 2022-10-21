---
theme: uncover
size: 16:9
marp: true
_class: invert
---

![w:160](https://freesvg.org/img/1520278248.png)

# **AI Project**

## A French poetry generator

A French poem generator based on [Project Gutenberg] dataset.

[project gutenberg]: https://www.gutenberg.org/


---
## Subject
Generating lines of verse from a few strating words.

The goal is to generate a poem that rimes, while using vocabulary from well-known French poets.

---
## Datasets
### Senetence generator
Raw text from around 30 books of french poetry from *Project Gutenberg*.
### Phonetic writing generator
French dictionnary with phonetic writing.

---

## Models
We will use a transformer model for our sentence generator. Our model is decoder-only, and will be trained with a language generation objective.

---

## Language & tools
  - Python
  - Jupyter
  - Tensorflow
