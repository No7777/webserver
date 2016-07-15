#-*-coding:utf-8-*-
import pymongo
import numpy as np

def cosVal(val1,val2):
    my1 = np.array(val1)
    my2 = np.array(val2)
    cos1 = np.sum(my1*my2)
    cos21 = np.sqrt(float(sum(my1*my1)))
    cos22 = np.sqrt(float(sum(my2*my2)))
    try:
        fin = cos1/(cos21*cos22)
    except:
        return 0
    return float('%0.3f'%fin)

class newsSearch():
    def __init__(self,title):
        self.title = title
        self.client = pymongo.MongoClient("mongodb://172.20.111.219:27017/")
        self.db = self.client.emotion_db           ###
        self.B1 = self.db.B1
        #self.B2 = self.db.B2
        #self.B3 = self.db.B3
        self.words = {}
        self.final = []

    def pre(self):
        mydict = self.B1.find_one({'title':self.title})
        if mydict != None:
            self.words = mydict['words']


    def process(self):
        if self.words == {}:
            return
        for news in self.B1.find({'num': {"$gt": 100}}):
            self.trend(news)

    def trend(self,news):
        val1 = []
        val2 = []
        words2 = news['words']
        for word in self.words:
            if self.words[word] == 1:
                continue
            val1.append(self.words[word])
            if word not in words2:
                val2.append(-1-int(self.words[word])/10)   ######
            else:
                val2.append(words2[word]-1-int(self.words[word])/10)
        cosval = cosVal(val1,val2)
        if cosval > 0.1:          #######
#           self.trend2(words2,news,val1,val2)
            self.final.append([news['title'],cosval, news['time'], news['num']])


    def trend2(self,words2,news,val1,val2):
        for word in words2:
            if word not in self.words:
                if words2[word]>1:   ####
                    val2.append(words2[word])
                    val1.append(-1-int(words2[word])/10)    ######
            else:
                if self.words[word] == 1 and words2[word]>1:
                    val2.append(words2[word])
                    val1.append(1-1-int(words2[word])/10)    ######
        #val1 = [x if( x < 6 )else( x/3 + 4 ) for x in val1]
        #val2 = [x if( x < 6 )else( x/3 + 4 ) for x in val2]
        cosval = cosVal(val1,val2)
        if cosval > 0.1 and news['title']!=self.title:     ######
            self.final.append([news['title'],cosval, news['time'], news['num']])

    def run(self):
        self.pre()
        self.process()
        return self.final
        #for i in self.final:
            #print i[0],i[1]


#a = newsSearch(u'魏则西父亲称百度公司说谎 从未联系过自己')
#a.run()
