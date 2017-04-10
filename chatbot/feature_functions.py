import json
import re

class feature_functions:

    def __init__(self):
        self.diseases = []
        self.symptoms = []
        self.time = []
        self.vaccines = []
        self.numbers = []
        self.allergy = []
        self.place = []
        self.unit = []
        self.metric = []
        self.wmap = dict()

        self.flist = (self.fDISEASE_1, self.fDISEASE_2, self.fDISEASE_3, self.fDISEASE_4, self.fDISEASE_5,self.fDISEASE_6,self.fSYMPTOM_1, self.fSYMPTOM_2, self.fSYMPTOM_3, self.fSYMPTOM_4, self.fSYMPTOM_5, self.fSYMPTOM_6,self.fTIME_1, self.fTIME_2, self.fVACCINE_1, self.fVACCINE_2, self.fVACCINE_3, self.fVACCINE_4, self.fNUMBER_1,self.fNUMBER_2, self.fALLERGY_1, self.fALLERGY_2, self.fALLERGY_3, self.fPLACE_1, self.fUNIT_1, self.fUNIT_2,self.fUNIT_3,self.fMETRIC_1)
        self.fdict = {}
        self.tags = ("ALLERGY","DISEASE","METRIC","NAME","NUMBER","OTHERS","PLACE","SYMPTOM","TIME","UNIT","VACCINE")
        #print (len(self.flist))
        for k, v in feature_functions.__dict__.items():
            if hasattr(v, "__call__"):
                if k[0] == 'f':
                    #self.flist[k] = v  # .append(v)
                    tag = k[1:].split("_")[0]
                    val = self.fdict.get(tag, [])
                    val.append(v)
                    self.fdict[tag] = val
        print (self.fdict)
        self.read_word_list()

    def read_word_list(self):
        fo = open('word_list.json', 'r')
        with fo as f:
            root = json.load(f)

        self.diseases = root["diseases"]
        self.symptoms = root["symptoms"]
        self.time = root["time"]
        self.vaccines = root["vaccines"]
        self.numbers = root["numbers"]
        self.allergy = root["allergy"]
        self.place = root["place"]
        self.unit = root["unit"]
        self.metric = root["metric"]

        print (self.diseases[:4])

        if self.diseases[0] == self.diseases[1]:
            print ("True")

    def set_wmap(self, wmap):
        self.wmap = wmap

    def evaluate(self, xi, tag):
        feats = []
        for t, f in self.fdict.items():
            if t == tag:
                for f1 in f:
                    feats.append(int(f1(self, xi, tag)))
            else:
                for f1 in f:
                    feats.append(0)
        return feats

    ''' x is a history tuple of word i of the form :-
    x = (ta, tb, wn, i),
    where x[0] = ta = tag of word i-2,
    x[1] = tb = tag of word i-1,
    x[2] = wn = index of sentence and
    x[3] = i = index of word;
    y is a tag'''

    #features for diseases tag
    def fDISEASE_1(self, x, y):
        try:
            if y=="DISEASE" and self.wmap[x[2]][x[3]] in self.diseases:
                return 1
        except:
            return 0
        return 0

    def fDISEASE_2(self, x, y):
        try:
            if y=="DISEASE" and self.wmap[x[2]][x[3]]+" "+self.wmap[x[2]][x[3]+1] in self.diseases:
                return 1
        except:
            return 0
        return 0

    def fDISEASE_3(self, x, y):
        try:
            if y=="DISEASE" and self.wmap[x[2]][x[3]-1]+" "+self.wmap[x[2]][x[3]] in self.diseases:
                return 1
        except:
            return 0
        return 0

    def fDISEASE_4(self, x, y):
        #handles cases like एच. आई. वी.  एड्स
        match = re.match(r'.*\.$',self.wmap[x[2]][x[3]])
        try:
            if y=="DISEASE" and match:
                return 1
        except:
            return 0
        return 0

    def fDISEASE_5(self, x, y):
        try:
            if y=="DISEASE" and ((self.wmap[x[2]][x[3]] in self.diseases and (self.wmap[x[2]][x[3]+1] =="रोग" or self.wmap[x[2]][x[3]+1] =="डिसीस" )) or (self.wmap[x[2]][x[3]]+" "+self.wmap[x[2]][x[3]+1] in self.diseases and (self.wmap[x[2]][x[3]+2] =="रोग" or self.wmap[x[2]][x[3]+2] =="डिसीस" )) or (self.wmap[x[3]][x[3]-1]+" "+self.wmap[x[3]][x[3]] in self.diseases and (self.wmap[x[2]][x[3]+1] =="रोग" or self.wmap[x[2]][x[3]+1] =="डिसीस" ))):
                return 1
        except:
            return 0
        return 0

    def fDISEASE_6(self, x, y):
        try:
            if y=="DISEASE" and (self.wmap[x[2]][x[3]+2]=="प्रमाण" or self.wmap[x[2]][x[3]+2]=="निशाना"):
                return 1
        except:
            return 0
        return 0

    #feature for symptom tag
    def fSYMPTOM_1(self, x, y):
        #print ("hai")
        try:
            if y=="SYMPTOM" and (self.wmap[x[2]][x[3]]=="दर्द" or self.wmap[x[2]][x[3]] in self.symptoms):
                #print("hai")
                return 1
        except:
            #print("hai")
            return 0
        #print("hai")
        return 0

    def fSYMPTOM_2(self, x, y):
        try:
            if y=="SYMPTOM" and self.wmap[x[2]][x[3]]+" "+self.wmap[x[2]][x[3]+1] in self.symptoms:
                return 1
        except:
            return 0
        return 0

    def fSYMPTOM_3(self, x, y):
        try:
            if y=="SYMPTOM" and self.wmap[x[2]][x[3]-1]+" "+self.wmap[x[2]][x[3]] in self.symptoms:
                return 1
        except:
            return 0
        return 0

    def fSYMPTOM_4(self, x, y):
        try:
            #print(self.wmap[x[2]][x[3]] + " " + self.wmap[x[2]][x[3]+1] + " " + self.wmap[x[2]][x[3]+2])
            if y=="SYMPTOM" and self.wmap[x[2]][x[3]]+" "+self.wmap[x[2]][x[3]+1]+" "+self.wmap[x[2]][x[3]+2] in self.symptoms:
                print ("hai")
                return 1
        except:
            return 0
        return 0

    def fSYMPTOM_5(self, x, y):
        try:

            if y=="SYMPTOM" and self.wmap[x[2]][x[3]-2]+" "+self.wmap[x[2]][x[3]-1]+" "+self.wmap[x[2]][x[3]] in self.symptoms:
                return 1
        except:
            return 0
        return 0

    def fSYMPTOM_6(self, x, y):
        try:
            if y=="SYMPTOM" and (self.wmap[x[2]][x[3]+1]=="में" or self.wmap[x[2]][x[3]+1]=="मे") and self.wmap[x[2]][x[3]+2]=="दर्द":
                return 1
        except:
            return 0
        return 0

    def fTIME_1(self, x, y):
        try:
            if y=="TIME" and self.wmap[x[2]][x[3]] in self.time:
                return 1
        except:
            return 0
        return 0
    #कुछ बहुत ज़्यादा
    def fTIME_2(self, x, y):
        try:
            if y=="TIME" and self.wmap[x[2]][x[3]] in ["कुछ","बहुत","ज़्यादा"] and self.wmap[x[2]][x[3]+1] in self.time :
                return 1
        except:
            return 0
        return 0

    def fVACCINE_1(self, x, y):
        try:
            if y=="VACCINE" and self.wmap[x[2]][x[3]] in self.vaccines:
                return 1
        except:
            return 0
        return 0

    def fVACCINE_2(self, x, y):
        try:
            if y=="VACCINE" and self.wmap[x[2]][x[3]+2] == "टीका" and self.wmap[x[2]][x[3]] in self.vaccines :
                return 1
        except:
            return 0
        return 0

    def fVACCINE_3(self, x, y):
        try:
            if y=="VACCINE" and self.wmap[x[2]][x[3]]+" "+self.wmap[x[2]][x[3]+1] in self.vaccines:
                return 1
        except:
            return 0
        return 0

    def fVACCINE_4(self, x, y):
        try:
            if y=="VACCINE" and self.wmap[x[2]][x[3]-1]+" "+self.wmap[x[2]][x[3]] in self.vaccines:
                return 1
        except:
            return 0
        return 0

    def fNUMBER_1(self, x, y):
        try:
            if y=="NUMBER" and self.wmap[x[2]][x[3]] in self.numbers:
                return 1
        except:
            return 0
        return 0

    def fNUMBER_2(self, x, y):
        try:
            if y=="NUMBER" and re.match(r"^\d+(\.\d+)?$",self.wmap[x[2]][x[3]]):
                return 1
        except:
            return 0
        return 0

    def fALLERGY_1(self, x, y):
        try:
            if y=="ALLERGY" and self.wmap[x[2]][x[3]] in self.allergy:
                return 1
        except:
            return 0
        return 0

    def fALLERGY_2(self, x, y):
        try:
            if y=="ALLERGY" and self.wmap[x[2]][x[3]]+" "+self.wmap[x[2]][x[3]+1] in self.allergy:
                return 1
        except:
            return 0
        return 0

    def fALLERGY_3(self, x, y):
        try:
            if y=="ALLERGY" and self.wmap[x[2]][x[3]-1]+" "+self.wmap[x[2]][x[3]] in self.allergy:
                return 1
        except:
            return 0
        return 0

    def fPLACE_1(self, x, y):
        try:
            if y=="PLACE" and self.wmap[x[2]][x[3]] in self.place:
                return 1
        except:
            return 0
        return 0

    def fUNIT_1(self, x, y):
        try:
            if y=="UNIT" and self.wmap[x[2]][x[3]] in self.unit:
                return 1
        except:
            return 0
        return 0

    def fUNIT_2(self, x, y):
        try:
            if y=="UNIT" and x[1]=="NUMBER":
                return 1
        except:
            return 0
        return 0

    def fUNIT_3(self, x, y):
        try:
            if y=="UNIT" and x[0]=="METRIC" and x[1]=="NUMBER":
                return 1
        except:
            return 0
        return 0

    def fMETRIC_1(self, x, y):
        try:
            if y=="METRIC" and self.wmap[x[2]][x[3]] in self.metric:
                return 1
        except:
            return 0
        return 0

#obj = feature_functions()
#obj.read_word_list()