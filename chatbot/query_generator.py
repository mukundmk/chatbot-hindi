from collections import defaultdict

__author__ = 'mukundmk'

known_tags = list(['ALLERGY', 'DISEASE', 'METRIC', 'NAME', 'NUMBER', 'OTHERS', 'PLACE', 'SYMPTOM', 'TIME', 'UNIT',
                   'VACCINE'])
known_words = dict()

with open('words.txt') as f:
    t = ''
    for l in f:
        if l.strip() in known_tags:
            t = l.strip()

        else:
            known_words[l.strip()] = t


def generate_queries(tagged_sentence):
    """
    Input: a list of (word, tag) tuples
    Output: a dictionary with relations to query the db
    """
    global known_words

    compressed_sentence = defaultdict(list)
    i = 0
    marked = list()
    sentence_length = len(tagged_sentence)
    while i < sentence_length:
        if i in marked:
            continue

        item = tuple(reversed(tagged_sentence[i]))

        if item[0] == 'NUMBER':
            if tagged_sentence[i + 1][1] == 'UNIT':
                j = i + 2
                while j < sentence_length:
                    if tagged_sentence[j][1] == 'UNIT':
                        compressed_sentence['METRIC'].append(
                            ('METRIC', item[1], tagged_sentence[i + 1][0], tagged_sentence[j][0], True))
                        marked.extend([i, i + 1, j])
                        break

                    j += 1

        elif item[0] == 'METRIC':
            j = i + 1
            while j < sentence_length - 1:
                if tagged_sentence[j][1] == 'NUMBER' and tagged_sentence[j + 1][1] == 'UNIT':
                    compressed_sentence['METRIC'].append(
                        ('METRIC', tagged_sentence[j][0], tagged_sentence[j + 1][0], item[1], True))
                    marked.extend([i, j, j + 1])
                    break
                j += 1

        elif item[1] in known_words:
            j = i + 1
            max_str = item[1]
            while j < sentence_length and tagged_sentence[j][1] == item[0] and \
                    max_str + ' ' + tagged_sentence[j][0] in known_words:
                max_str = max_str + ' ' + tagged_sentence[j][0]
                j += 1

            compressed_sentence[item[0]].append((item[0], max_str, True))
            i = j

        else:
            compressed_sentence[item[0]].append((*item, False))
            i += 1

        queries = list()
        # TODO: queries based on how db is structured
        return queries
