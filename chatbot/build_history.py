'''import json
import feature_functions
import MyMaxEnt
import MyViterbi

def build_history(data_list, supported_tags):
    history_list = []  # list of all histories
    words_map = {}
    count = 0
    count_list = []
    index = 0
    for data in data_list:  # data is the inputs entered by a given student
        data1 = data['data']
        for rec in data1:
            updates = rec['updates']
            sent = rec['sentence']
            words = []

            for i in range(len(updates)):
                words.append(updates[i]['word'])
                # ------------------------------------------------------------------------------------------------
                # NOTE: below code is a temporary hack to build the MAxEnt for just 2 tags - we will change this later
                if (updates[i]['tag'] == "Model"):
                    updates[i]['tag'] = "Version"
                elif (updates[i]['tag'] == "Size"):
                    updates[i]['tag'] = "Feature"
                elif (updates[i]['tag'] not in supported_tags):
                    updates[i]['tag'] = "Other"

                    # ------------------------------------------------------------------------------------------------

            words_map[count] = {'words': words}  # , 'pos_tags': nltk.pos_tag(words)}

            len_sent = len(words)
            if index == 0:
                count_list.append(len_sent)
            else:
                count_list.append(count_list[index - 1] + len_sent)
            index += 1

            for i in range(len(updates)):
                history = {}
                history["i"] = i
                if i == 0:
                    history["ta"] = "*"  # special tag
                    history["tb"] = "*"  # special tag
                elif i == 1:
                    history["ta"] = "*"  # special tag
                    history["tb"] = updates[i - 1]['tag']
                else:
                    history["ta"] = updates[i - 2]['tag']
                    history["tb"] = updates[i - 1]['tag']
                history["wn"] = count
                history_list.append((history, updates[i]['tag'],))
            count += 1
    return (history_list, words_map, count_list)


def test(clf, history_list, wmap):
    result = []
    for history in history_list:
        mymap = self.wmap[history[0]["wn"]]
        words = mymap['words']
        # tags = mymap['pos_tags']
        index = history[0]["i"]
        val = clf.classify(history[0])
        result.append({'predicted': val, 'word': words[index], 'expected': history[1]})
    return result


if __name__ == "__main__":
    pass
    # ----- REPLACE THESE PATHS FOR YOUR SYSTEM ---------------------
    json_file = r"all_data.json"
    pickle_file = r"all_data.p"
    # ----------------------------------------------------------------

    TRAIN = 1 #int(raw_input("Enter 1 for Train, 0 to use pickeled file:  "))
    supported_tags = ["Org", "OS", "Version", "Family", "Price", "Phone", "Feature" ,"Other"]

    tag_set = {"Org": 0, "Other": 1}
    dims = 9
    trg_data_x = []
    trg_data_y = []
    trg_data = {'Org': [], 'Other': []}
    data = json.loads(open(json_file).read())['root']

    (history_list, wmap, count_list) = build_history(data[0:70], supported_tags)
    print "After build_history"
    func_obj = feature_functions()#, supported_tags)
    func_obj.set_wmap(wmap)
    clf = MyMaxEnt(history_list, func_obj, reg_lambda = 0.001, pic_file = pickle_file)
    print clf.model
    if TRAIN == 1:
       clf.train()
    
    result = test(clf, history_list[-500:])
    count_correct=0
    for r in result:
        print r['word'], r['predicted'], r['expected']
        if r['predicted'] == r['expected']:
            count_correct+=1
    print count_correct
    
    
    tagged_sentences = []
    predicted = []
    for num in range(1, 1300):
        h_list = history_list[count_list[num-1]+1:count_list[num]+1]
        tagged_sentence=[]
        sentence_words = wmap[num]["words"]
        path=Viterbi(sentence_words, clf, supported_tags, h_list)
        print path
        for index in range(len(sentence_words)):
            tagged_sentence.append(h_list[index][1])
        tagged_sentences.append(tagged_sentence)
        predicted.append(path)
    ner=ner_metrics.NerMetrics(tagged_sentences,predicted)
    metrics=ner.compute()
    print "Metrics", metrics
    ner.print_results()'''
