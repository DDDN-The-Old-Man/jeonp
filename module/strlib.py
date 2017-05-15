from difflib import SequenceMatcher

def decode_text(text):
    decoded = False
    types = ['utf-8', 'euc-kr']
    for t in types:
        try:
            text = text.decode(t)
            decoded = True
        except:
            pass
        if decoded:
            break

    if decoded:
        return text
    return str(text)

def get_similarity(text1, text2):
    seq = SequenceMatcher(None, text1, text2)
    r = seq.ratio() / 2
    r *= len(text1) + len(text2)
    r /= len(text1)
    return r

def find_similar(pickle_path, query):
    nlp = NLProcessor()
    c2 = nlp.nlplib.pos(query)
    pprint(c2)

    with open(pickle_path, 'rb') as f:
        texts = pickle.load(f)

    result = []

    for text in texts:
        if not text:
            continue
        c = nlp.nlplib.pos(text)
        ss = nlp.get_sentence(c)
        seq = SequenceMatcher(None, c2)
        for s in ss:
            seq.set_seq2(s)
            r = seq.ratio()
            r = r / 2
            r *= len(c2) + len(s)
            r /= len(c2)
            if r >= 0.6:
                result.append((query, s, c, int(r*100000)/1000, text))
    return result
