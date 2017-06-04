import pickle

class SimSen():
    WORD_SIM_PICKLE = 'sim.pickle'
    with open(WORD_SIM_PICKLE, 'rb') as f:
        wv = pickle.load(f)

    def sim_val(w1, w2):
        if w1 == w2:
            return 1.0
        if w1 in SimSen.wv and w2 in SimSen.wv:
            v = 0.0
            for i in range(128):
                v += SimSen.wv[w1][i]*SimSen.wv[w2][i]
            if v<0:
                v = v * (-1)
            return v
        return 0.0


    def similarity(q_seq, t_seq):
        ql = len(q_seq)
        tl = len(t_seq)
        d = [ [ -1000000.0 for _ in range(tl+1) ] for _ in range(ql+1) ]
        d[0][0] = 0.0
        h = [ [ -1 for _ in range(tl+1) ] for _ in range(ql+1) ]
        for i in range(ql+1):
            for j in range(tl+1):
                if i<ql and d[i+1][j] < d[i][j] - 0.1:
                    d[i+1][j] = d[i][j] - 0.1
                if j<tl and d[i][j+1] < d[i][j] - 0.01:
                    d[i][j+1] = d[i][j] - 0.01
                if i<ql and j<tl:
                    v = SimSen.sim_val(q_seq[i], t_seq[j])
                    if v < 0.1:
                        continue
                    if d[i+1][j+1] < d[i][j] + v:
                        d[i+1][j+1] = d[i][j] + v
        sim = d[ql][tl] / (len(q_seq) + 1)
        if sim < 0.0:
            sim = 0.0
        if sim >= 1.0:
            sim = 1.0 - sim*0.02
        return sim
