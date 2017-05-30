from difflib import SequenceMatcher
from module.simsen import SimSen

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

