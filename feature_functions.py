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

        self.flist = (self.fdiseases_1, self.fdiseases_2, self.fdiseases_3, self.fdiseases_4, self.fdiseases_5,self.fdiseases_6,self.fsymptoms_1, self.fsymptoms_2, self.fsymptoms_3, self.fsymptoms_4, self.fsymptoms_5, self.fsymptoms_6,self.ftime_1, self.ftime_2, self.fvaccine_1, self.fvaccine_2, self.fvaccine_3, self.fvaccine_4, self.fnumber_1,self.fnumber_2, self.fallergy_1, self.fallergy_2, self.fallergy_3, self.fplace_1, self.funit_1, self.funit_2,self.funit_3,self.fmetric_1)

        self.tags = ("ALLERGY","DISEASE","METRIC","NAME","NUMBER","OTHERS","PLACE","SYMPTOM","TIME","UNIT","VACCINE")
        #print (len(self.flist))

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
    def fdiseases_1(self, x, y):
        try:
            if y=="DISEASE" and self.wmap[x[2]][x[3]] in self.diseases:
                return 1
        except:
            return 0
        return 0

    def fdiseases_2(self, x, y):
        try:
            if y=="DISEASE" and self.wmap[x[2]][x[3]]+" "+self.wmap[x[2]][x[3]+1] in self.diseases:
                return 1
        except:
            return 0
        return 0

    def fdiseases_3(self, x, y):
        try:
            if y=="DISEASE" and self.wmap[x[2]][x[3]-1]+" "+self.wmap[x[2]][x[3]] in self.diseases:
                return 1
        except:
            return 0
        return 0

    def fdiseases_4(self, x, y):
        #handles cases like एच. आई. वी.  एड्स
        match = re.match(r'.*\.$',self.wmap[x[2]][x[3]])
        try:
            if y=="DISEASE" and match:
                return 1
        except:
            return 0
        return 0

    def fdiseases_5(self, x, y):
        try:
            if y=="DISEASE" and ((self.wmap[x[2]][x[3]] in self.diseases and (self.wmap[x[2]][x[3]+1] =="रोग" or self.wmap[x[2]][x[3]+1] =="डिसीस" )) or (self.wmap[x[2]][x[3]]+" "+self.wmap[x[2]][x[3]+1] in self.diseases and (self.wmap[x[2]][x[3]+2] =="रोग" or self.wmap[x[2]][x[3]+2] =="डिसीस" )) or (self.wmap[x[3]][x[3]-1]+" "+self.wmap[x[3]][x[3]] in self.diseases and (self.wmap[x[2]][x[3]+1] =="रोग" or self.wmap[x[2]][x[3]+1] =="डिसीस" ))):
                return 1
        except:
            return 0
        return 0

    def fdiseases_6(self, x, y):
        try:
            if y=="DISEASE" and (self.wmap[x[2]][x[3]+2]=="प्रमाण" or self.wmap[x[2]][x[3]+2]=="निशाना"):
                return 1
        except:
            return 0
        return 0

    #feature for symptom tag
    def fsymptoms_1(self, x, y):
        try:
            if y=="SYMPTOM" and (self.wmap[x[2]][x[3]]=="दर्द" or self.wmap[x[2]][x[3]] in self.symptoms):
                return 1
        except:
            return 0
        return 0

    def fsymptoms_2(self, x, y):
        try:
            if y=="SYMPTOM" and self.wmap[x[2]][x[3]]+" "+self.wmap[x[2]][x[3]+1] in self.symptoms:
                return 1
        except:
            return 0
        return 0

    def fsymptoms_3(self, x, y):
        try:
            if y=="SYMPTOM" and self.wmap[x[2]][x[3]-1]+" "+self.wmap[x[2]][x[3]] in self.symptoms:
                return 1
        except:
            return 0
        return 0

    def fsymptoms_4(self, x, y):
        try:
            if y=="SYMPTOM" and self.wmap[x[2]][x[3]]+" "+self.wmap[x[2]][x[3]+1]+" "+self.wmap[x[2]][x[3]+2] in self.symptoms:
                return 1
        except:
            return 0
        return 0

    def fsymptoms_5(self, x, y):
        try:
            if y=="SYMPTOM" and self.wmap[x[2]][x[3]-2]+" "+self.wmap[x[2]][x[3]-1]+" "+self.wmap[x[2]][x[3]+2] in self.symptoms:
                return 1
        except:
            return 0
        return 0

    def fsymptoms_6(self, x, y):
        try:
            if y=="SYMPTOM" and (self.wmap[x[2]][x[3]+1]=="में" or self.wmap[x[2]][x[3]+1]=="मे") and self.wmap[x[2]][x[3]+2]=="दर्द":
                return 1
        except:
            return 0

    def ftime_1(self, x, y):
        try:
            if y=="TIME" and self.wmap[x[2]][x[3]] in self.time:
                return 1
        except:
            return 0
        return 0
    #कुछ बहुत ज़्यादा
    def ftime_2(self, x, y):
        try:
            if y=="TIME" and self.wmap[x[2]][x[3]] in ["कुछ","बहुत","ज़्यादा"] and self.wmap[x[2]][x[3]+1] in self.time :
                return 1
        except:
            return 0
        return 0

    def fvaccine_1(self, x, y):
        try:
            if y=="VACCINE" and self.wmap[x[2]][x[3]] in self.vaccines:
                return 1
        except:
            return 0
        return 0

    def fvaccine_2(self, x, y):
        try:
            if y=="VACCINE" and self.wmap[x[2]][x[3]+2] == "टीका" and self.wmap[x[2]][x[3]] in self.vaccines :
                return 1
        except:
            return 0
        return 0

    def fvaccine_3(self, x, y):
        try:
            if y=="VACCINE" and self.wmap[x[2]][x[3]]+" "+self.wmap[x[2]][x[3]+1] in self.vaccines:
                return 1
        except:
            return 0
        return 0

    def fvaccine_4(self, x, y):
        try:
            if y=="VACCINE" and self.wmap[x[2]][x[3]-1]+" "+self.wmap[x[2]][x[3]] in self.vaccines:
                return 1
        except:
            return 0
        return 0

    def fnumber_1(self, x, y):
        try:
            if y=="NUMBER" and self.wmap[x[2]][x[3]] in self.numbers:
                return 1
        except:
            return 0
        return 0

    def fnumber_2(self, x, y):
        try:
            if y=="NUMBER" and re.match(r"^\d+(\.\d+)?$",self.wmap[x[2]][x[3]]):
                return 1
        except:
            return 0
        return 0

    def fallergy_1(self, x, y):
        try:
            if y=="ALLERGY" and self.wmap[x[2]][x[3]] in self.allergy:
                return 1
        except:
            return 0
        return 0

    def fallergy_2(self, x, y):
        try:
            if y=="ALLERGY" and self.wmap[x[2]][x[3]]+" "+self.wmap[x[2]][x[3]+1] in self.allergy:
                return 1
        except:
            return 0
        return 0

    def fallergy_3(self, x, y):
        try:
            if y=="ALLERGY" and self.wmap[x[2]][x[3]-1]+" "+self.wmap[x[2]][x[3]] in self.allergy:
                return 1
        except:
            return 0
        return 0

    def fplace_1(self, x, y):
        try:
            if y=="PLACE" and self.wmap[x[2]][x[3]] in self.place:
                return 1
        except:
            return 0
        return 0

    def funit_1(self, x, y):
        try:
            if y=="UNIT" and self.wmap[x[2]][x[3]] in self.unit:
                return 1
        except:
            return 0
        return 0

    def funit_2(self, x, y):
        try:
            if y=="UNIT" and x[1]=="NUMBER":
                return 1
        except:
            return 0
        return 0

    def funit_3(self, x, y):
        try:
            if y=="UNIT" and x[0]=="METRIC" and x[1]=="NUMBER":
                return 1
        except:
            return 0
        return 0

    def fmetric_1(self, x, y):
        try:
            if y=="METRIC" and self.wmap[x[2]][x[3]] in self.metric:
                return 1
        except:
            return 0
        return 0

obj = feature_functions()
obj.read_word_list()