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


def compress_sentence(tagged_sentence):
    """
    Input: a list of (word, tag) tuples
    Output: a dictionary with relations to query the db
    """
    global known_words

    compressed_sentence = defaultdict(set)
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
                        compressed_sentence['METRIC'].add(
                            ('METRIC', item[1], tagged_sentence[i + 1][0], tagged_sentence[j][0], True))
                        marked.extend([i, i + 1, j])
                        break

                    j += 1
            i += 1

        elif item[0] == 'METRIC':
            j = i + 1
            while j < sentence_length - 1:
                if tagged_sentence[j][1] == 'NUMBER' and tagged_sentence[j + 1][1] == 'UNIT':
                    compressed_sentence['METRIC'].add(
                        ('METRIC', tagged_sentence[j][0], tagged_sentence[j + 1][0], item[1], True))
                    marked.extend([i, j, j + 1])
                    break
                j += 1
            i += 1

        else:
            j = i + 1
            max_str = item[1]
            concat = item[1]
            pos = j
            while j < sentence_length and (tagged_sentence[j][1] == item[0] or tagged_sentence[j][0] == 'में'):
                concat += ' ' + tagged_sentence[j][0]
                j += 1
                if concat in known_words:
                    pos = j
                    max_str = concat

            compressed_sentence[item[0]].add((item[0], max_str, True))
            i = pos

    for i in compressed_sentence:
        compressed_sentence[i] = list(compressed_sentence[i])

    return compressed_sentence


def response_positive(tagged_sentence):
    for i in tagged_sentence:
        if i[0] in ['हाँ', 'हां', 'जी']:
            return True

    return False


def find(compressed_sentence, mongo_collection, context):
    response_data = dict()
    posts = mongo_collection.find(context['symptoms'])
    if posts.count() == 0:
        response_data['template_key'] = "2"
        response_data['template_data'] = {}
        return response_data, None

    n = max(posts, key=lambda x: x['Riskfactor'])
    for j in n['Symptoms']:
        if 'Symptoms.' + j not in context['symptoms']:
            response_data['template_key'] = "3"
            response_data['template_data'] = {'symptom': j}
            context['cur'] = ('SYMPTOM', j)
            if 'DISEASE' in compressed_sentence:
                context['Disease'] = compressed_sentence['DISEASE']
            else:
                context['Disease'] = []
            return response_data, context

    for i in compressed_sentence['DISEASE']:
        if i[1] == n['Disease']:
            response_data['template_key'] = "4"
            response_data['template_data'] = {'disease': n['Disease'], 'place': n['Place'],
                                              'doctor': n.get('Doctors')}

            return response_data, None

    if compressed_sentence['DISEASE']:
        response_data['template_key'] = "5"
        response_data['template_data'] = {'disease': n['Disease'], 'place': n['Place'],
                                          'doctor': n.get('Doctors')}

        return response_data, None

    response_data['template_key'] = "6"
    response_data['template_data'] = {'disease': n['Disease'], 'place': n['Place'],
                                      'doctor': n.get('Doctors')}

    return response_data, None


def enquire(tagged_sentence, mongo_collection, context=None):
    response_data = dict()
    if context is None:
        context = defaultdict(dict)
        compressed_sentence = compress_sentence(tagged_sentence)
        if not compressed_sentence['SYMPTOM']:
            response_data['template_key'] = "1"
            response_data['template_data'] = {}
            return response_data, None

        for i in compressed_sentence['SYMPTOM']:
            if i[2]:
                context['symptoms']['Symptoms.' + i[1]] = {'$exists': True}

        return find(compressed_sentence, mongo_collection, context)

    else:
        pos = response_positive(tagged_sentence)
        if pos:
            context['symptoms']['Symptoms.' + context['cur'][1]] = {'$exists': True}
            return find({'DISEASE': context['Disease']}, mongo_collection, context)

        context['symptoms']['Symptoms.' + context['cur'][1]] = {'$exists': False}
        return find({'DISEASE': context['Disease']}, mongo_collection, context)


if __name__ == "__main__":
    from pymongo import MongoClient
    from nlg import generate_sentence

    client = MongoClient('mongodb://localhost:27017/')

    # Test
    sent = [('नमस्ते', 'OTHER')]
    print('User:', ' '.join([x[0] for x in sent]))
    response, context = enquire(sent, client.chatbot.medicaldata)
    print('Bot:', generate_sentence(response['template_key'], response['template_data']))
    sent = [('मुझे', 'OTHER'), ('कल', 'TIME'), ('सुबह', 'TIME'), ('से', 'OTHER'), ('फीवर', 'SYMPTOM'), ('है', 'OTHER')]
    print('User:', ' '.join([x[0] for x in sent]))git
    response, context = enquire(sent, client.chatbot.medicaldata, context)
    print('Bot:', generate_sentence(response['template_key'], response['template_data']))
    sent = [('हाँ', 'OTHER'), ('मुझे', 'OTHER'), ('है', 'OTHER')]
    # sent = [('मुझे', 'OTHER'), ('नहीं', 'OTHER'), ('है', 'OTHER')]
    print('User:', ' '.join([x[0] for x in sent]))
    response, context = enquire(sent, client.chatbot.medicaldata, context)
    print('Bot:', generate_sentence(response['template_key'], response['template_data']))
    sent = [('हाँ', 'OTHER'), ('मुझे', 'OTHER'), ('है', 'OTHER')]
    print('User:', ' '.join([x[0] for x in sent]))
    response, context = enquire(sent, client.chatbot.medicaldata, context)
    print('Bot:', generate_sentence(response['template_key'], response['template_data']))
    sent = [('हाँ', 'OTHER'), ('मुझे', 'OTHER'), ('है', 'OTHER')]
    print('User:', ' '.join([x[0] for x in sent]))
    response, context = enquire(sent, client.chatbot.medicaldata, context)
    print('Bot:', generate_sentence(response['template_key'], response['template_data']))
    sent = [('हाँ', 'OTHER'), ('मुझे', 'OTHER'), ('है', 'OTHER')]
    print('User:', ' '.join([x[0] for x in sent]))
    response, context = enquire(sent, client.chatbot.medicaldata, context)
    print('Bot:', generate_sentence(response['template_key'], response['template_data']))
    sent = [('हाँ', 'OTHER'), ('मुझे', 'OTHER'), ('है', 'OTHER')]
    # print('User:', ' '.join([x[0] for x in sent]))
    # response, context = enquire(sent, client.chatbot.medicaldata, context)
    # print('Bot:', generate_sentence(response['template_key'], response['template_data']))
