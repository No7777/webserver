#-*-coding:utf-8-*-
import pymongo


class search():
    def __init__(self,content):
        self.client = pymongo.MongoClient("mongodb://172.20.111.219:27017/")
        self.db = self.client.emotion_db           
        self.db_wbtopic = self.db.A2
        self.db_wbhot = self.db.A4
        self.db_news = self.db.B1
        self.content = content
        self.news = []
        self.wbtopic = []
        self.wbhot = []

    def process(self):
        for i in self.db_news.find({'title':{'$regex':self.content}}):
            tim = i['time'][0:4]+i['time'][5:7]+i['time'][8:10]
            self.news.append([i['title'],tim])
        for i in self.db_wbtopic.find({'topic':{'$regex':self.content}}):
            tim = i['history'][-1][0]
            tim = tim[0:4]+tim[5:7]+tim[8:10]
            self.wbtopic.append([i['topic'],tim])
        for i in self.db_wbhot.find({'topic':{'$regex':self.content}}):
            tim = i['history'][-1][0]
            tim = tim[0:4]+tim[5:7]+tim[8:10]
            self.wbhot.append([i['topic'],tim])

        self.news = sorted(self.news,key =lambda x:x[1],reverse = True)
        self.wbtopic = sorted(self.wbtopic,key =lambda x:x[1],reverse = True)
        self.wbhot = sorted(self.wbhot,key =lambda x:x[1],reverse = True)

    def run(self):
        self.process()

    def show(self):
        print "news:"
        for i in self.news:
            print i[0],i[1]
        print "wbtopic:"
        for i in self.wbtopic:
            print i[0],i[1]
        print "wbhot:"
        for i in self.wbhot:
            print i[0],i[1]

'''
a = search(u'南海')
a.run()
a.show()
'''
