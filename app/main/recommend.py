#-*-coding:utf-8-*-
import pymongo
import datetime
import random

class newsRecommend():
    def __init__(self,user):
        self.client=pymongo.MongoClient("mongodb://172.20.111.219:27017/")
        self.db = self.client.emotion_db           ###
        self.C1 = self.db.C1
        self.C2 = self.db.C2
        self.B4 = self.db.B4
        self.user = user
        self.today = datetime.date.today() ###
        self.DAYS = 3  #
        self.his = []
        self.tod = []
        self.rec = []

    def pre(self):
        today = str(self.today)[0:4]+str(self.today)[5:7]+str(self.today)[8:10]
        dict1 = self.C1.find_one({'user':self.user})
        if today in dict1['news']:
            self.tod = dict1['news'][today]
            self.tod.reverse()
            self.tod = self.tod[0:10]

        dict2 = self.C2.find_one({'user':self.user})
        if dict2:
            for i in xrange(self.DAYS):
                date = self.today - datetime.timedelta(days=i)
                date = str(date)[0:4]+str(date)[5:7]+str(date)[8:10]
                if dict2['time'] == date:
                    self.his = dict2['news']
                    break

    def process(self):
        k1 = len(self.his)
        items = [i for i in xrange(k1)]
        if k1 > 10:
            random.shuffle(items)
            k1 = 10
        for i in xrange(k1):
            news = self.his[items[i]]
            if news not in self.tod:
                if news not in self.rec:
                    self.rec.append(news)

        tmp = []
        for i in self.tod:
            tmpdict = self.B4.find_one({'title':i})
            if tmpdict:
                tmp.extend(tmpdict['list'])
        k2 = len(tmp)
        items = [i for i in xrange(k2)]
        if k2 > 10:
            random.shuffle(items)
            k2 = 10
        for i in xrange(k2):
            news = tmp[items[i]]
            if news not in self.tod:
                if news not in self.rec:
                    self.rec.append(news)


    def run(self):
        if not self.C1.find_one({'user':self.user}):
            return
        self.pre()
        self.process()
        return self.rec

    def show(self):
        for i in self.rec:
            print i

class wbtopicRecommend():
    def __init__(self,user):
        self.client=pymongo.MongoClient("mongodb://172.20.111.219:27017/")
        self.db = self.client.emotion_db           ###
        self.C1 = self.db.C1
        self.C2 = self.db.C2
        self.user = user
        self.today = datetime.date.today() ###
        self.DAYS = 3  #
        self.his = []
        self.tod = []
        self.rec = []

    def pre(self):
        today = str(self.today)[0:4]+str(self.today)[5:7]+str(self.today)[8:10]
        dict1 = self.C1.find_one({'user':self.user})
        if today in dict1['wbtopic']:
            self.tod = dict1['wbtopic'][today]
            self.tod.reverse()
            self.tod = self.tod[0:10]

        dict2 = self.C2.find_one({'user':self.user})
        if dict2:
            for i in xrange(self.DAYS):
                date = self.today - datetime.timedelta(days=i)
                date = str(date)[0:4]+str(date)[5:7]+str(date)[8:10]
                if dict2['time'] == date:
                    self.his = dict2['wbtopic']
                    break

    def process(self):
        k1 = len(self.his)
        items = [i for i in xrange(k1)]
        if k1 > 10:
            random.shuffle(items)
            k1 = 10
        for i in xrange(k1):
            weibo = self.his[items[i]]
            if weibo not in self.rec:
                self.rec.append(weibo)
        '''
        tmp = []
        for i in self.tod:
            tmpdict = self.B4.find_one({'title':i})
            if tmpdict:
                tmp.extend(tmpdict['list'])
        k2 = len(tmp)
        items = [i for i in xrange(k2)]
        if k2 > 10:
            random.shuffle(items)
            k2 = 10
        for i in xrange(k2):
            news = tmp[items[i]]
            if news not in self.tod:
                if news not in self.rec:
                    self.rec.append(news)
        '''


    def run(self):
        if not self.C1.find_one({'user':self.user}):
            return
        self.pre()
        self.process()
        return self.rec

    def show(self):
        for i in self.rec:
            print i

class wbhotRecommend():
    def __init__(self,user):
        self.client=pymongo.MongoClient("mongodb://172.20.111.219:27017/")
        self.db = self.client.emotion_db           ###
        self.C1 = self.db.C1
        self.C2 = self.db.C2
        self.user = user
        self.today = datetime.date.today() ###
        self.DAYS = 3  #
        self.his = []
        self.tod = []
        self.rec = []

    def pre(self):
        today = str(self.today)[0:4]+str(self.today)[5:7]+str(self.today)[8:10]
        dict1 = self.C1.find_one({'user':self.user})
        if today in dict1['wbhot']:
            self.tod = dict1['wbhot'][today]
            self.tod.reverse()
            self.tod = self.tod[0:10]

        dict2 = self.C2.find_one({'user':self.user})
        if dict2:
            for i in xrange(self.DAYS):
                date = self.today - datetime.timedelta(days=i)
                date = str(date)[0:4]+str(date)[5:7]+str(date)[8:10]
                if dict2['time'] == date:
                    self.his = dict2['wbhot']
                    break

    def process(self):
        k1 = len(self.his)
        items = [i for i in xrange(k1)]
        if k1 > 10:
            random.shuffle(items)
            k1 = 10
        for i in xrange(k1):
            weibo = self.his[items[i]]
            if weibo not in self.rec:
                self.rec.append(weibo)

    def run(self):
        if not self.C1.find_one({'user':self.user}):
            return
        self.pre()
        self.process()
        return self.rec

    def show(self):
        for i in self.rec:
            print i

'''
a = wbhotRecommend('a')
a.run()
a.show()
'''
