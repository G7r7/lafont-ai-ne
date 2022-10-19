import re

def poem_selection(path, filename):
  with open(path,'r') as file_stream:
    text = file_stream.read()
    paragraphes = re.split(r"\n{2,}", text)

    poems = [paragraphe for paragraphe in paragraphes if paragraphe.count('\n') > 1]

    id = 0
    for poem in poems:
      with open('poems/' + filename + str(id) + '.txt','wb') as poem_stream:
        poem_stream.write(poem.encode())
      id += 1

  return 0