import spacy
from collections import Counter, defaultdict
import msgpack

nlp = spacy.load('en_core_web_sm')

doc = nlp("The sky is literally literal falling fall, 53dawn, flew falled fell down, lol")

print([t.lemma_ for t in doc if t.is_alpha and not t.is_stop])

doc: list = [{"id":1, "name":"anna banna canna", "desc":" ", "abilities":"Anna Sergeyevna Dolgorukaya (1719–1778) was a Russian pedagogue, noble and courtier. She was the first principal of the Smolny Institute in Saint Petersburg in 1764–1764"},
             {"id":2, "name":"rj", "desc":"A fairy fighting type pokemon", "abilities":"Can can delete army delete an army of djs"},
             {"id":3, "name":"rd", "desc":"A Ice fairy type pokemon", "abilities":"Drinks water to stay hydrated"},
             {"id":4, "name":"rdj", "desc":"An electric Flying Steel type pokemon", "abilities":"Has a special move that can literally save the entire world when used"},
             {"id":5, "name":"rt", "desc":"An Ancient type pokemon", "abilities":"Can get you cancelled"}]

doc2: list = [{"id":1, "name":"rh", "desc":"A fire flying type pokemon", "abilities":"53dawn 5 Can spawn an entire village when called"},
             {"id":2, "name":"rj", "desc":"A fairy fighting type pokemon", "abilities":"Can can delete army delete an army of djs"},
             {"id":3, "name":"rd", "desc":"A Ice fairy type pokemon", "abilities":"Drinks water to stay hydrated"},
             {"id":4, "name":"rdj", "desc":"An electric Flying Steel type pokemon", "abilities":"Has a special move that can literally save the entire world when used"},
             {"id":5, "name":"rt", "desc":"An Ancient type pokemon", "abilities":"Can get you cancelled"}]

unique_words: dict = {}

for idx, sentence in enumerate(doc):
    id: int = sentence["id"]
    name: str = sentence["name"]
    desc: str = sentence["desc"]
    abilities: str = sentence["abilities"]
    alinol: dict = Counter([t.lemma_ for t in nlp(" ".join([name, desc, abilities])) if not t.is_stop and not t.is_digit])
    for w in alinol:
        if w not in unique_words:
            unique_words[w] = msgpack.packb([])
        # print(w, idx)
        a = msgpack.unpackb(unique_words[w])
        a.append([idx, alinol[w]])
        print(a, w)
        
        unique_words[w] = msgpack.packb(a)
    print("\nnextline\n")

print(unique_words)