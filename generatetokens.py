import spacy


def generate_tokens(text):
    ginza = spacy.load("ja_ginza")
    doc = ginza(text)

    for sent in doc.sents:
        for token in sent:
            yield token


sumple2 = generate_tokens("./database2.txt")
print(next(sumple2))
