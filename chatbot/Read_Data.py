'''reading the data'''
def reading_data(filename):
    raw_training_data = open(filename,"r")
    sentences = raw_training_data.readlines()
    #formatData = {}
    wordlist = []
    historylist = []
    count = 0
    count_list = []

    for index in range(len(sentences)):
        wordListPerSentence = []
        previos2 = "*"
        previos = "*"
        wordtag = sentences[index].split(" ")
        for wordtagindex in range(len(wordtag)):
            wordtagsplit = wordtag[wordtagindex].rsplit("/",1)
            wordListPerSentence.append(wordtagsplit[0])
            wordtuple = (previos2,previos,index,wordtagindex)
            wordtagtuple = (wordtuple,wordtagsplit[1])
            previos2 = previos
            previos = wordtagsplit[1]
            historylist.append(wordtagtuple)
        wordlist.append(wordListPerSentence)

        len_sent = len(wordtag)
        if index == 0:
            count_list.append(len_sent)
        else:
            count_list.append(count_list[index - 1] + len_sent)


        #formatData["history"] = historylist
    #formatData["wordList"] = wordList
    return (wordlist,historylist,count_list)

#formattedData = reading_data()
#print (formattedData)


