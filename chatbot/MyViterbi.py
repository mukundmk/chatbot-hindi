from collections import defaultdict


class MyViterbi():
    def Viterbi(self, sentence, q, tag_set, htuple):
        bp = {}
        vit = {}
        X = []
        X.append(0)
        for h in htuple:
            X.append(h[0])

        for k in range(0, len(sentence) + 1):
            bp[k] = defaultdict(lambda: defaultdict(lambda: "*"))

        for k in range(0, len(sentence) + 1):
            vit[k] = defaultdict(lambda: defaultdict(lambda: 1))

        for k in range(1, len(sentence) + 1):
            for v in tag_set:
                for u in tag_set:
                    (vit[k][u][v], bp[k][v][u]) = max((vit[k - 1][t][u] * q.p_y_given_x(X[k], v), t) for t in tag_set)
        max_v = 0
        t_1 = '*'
        t_2 = '*'
        for v in tag_set:
            for u in tag_set:
                if vit[len(sentence)][u][v] > max_v:
                    max_v = vit[len(sentence)][u][v]
                    t_1 = u
                    t_2 = v
        tag_seq = []
        for i in range(len(sentence) + 1):
            tag_seq.append(0)
        k = len(sentence)
        tag_seq[k - 1] = t_1
        tag_seq[k] = t_2
        k = k - 2
        while k > 0:
            tag_seq[k] = bp[k + 2][tag_seq[k + 1]][tag_seq[k + 2]]
            k -= 1

        return tag_seq[1:]