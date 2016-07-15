# -*-coding:utf-8-*-
import sys
from flask import render_template, redirect, url_for, request, session
from . import news
import json
from collections import OrderedDict
from .. import emotion_db
#from newsSearch import newsSearch
import datetime
from flask.ext.login import current_user
reload(sys)
sys.setdefaultencoding('utf8')
today = datetime.date.today()
today = str(today)[0:4]+str(today)[5:7]+str(today)[8:10]


@news.route('/newslist', methods=['GET', 'POST'])
def newslist():
    time = ''
    dic = {}
    if request.method == 'POST':
        time_str = request.form['time'].replace('-', '')
        session['newslist_time'] = time_str
        return redirect(url_for('news.newslist'))
    if 'newslist_time' in session:
        time_str = session['newslist_time']
        b2 = emotion_db.B2.find_one({'time': time_str})
        if not b2:
            del session['newslist_time']
            return 'Not Found'
        for news_list in b2['hot']:
            news_title = news_list[0]
            news_heat = news_list[1]
            dic[news_title] = news_heat
    else:
        time = datetime.datetime.now()
        while True:
            time_str = str(time)[:10].replace('-', '')
            b2 = emotion_db.B2.find_one({'time': str(time_str)})  # B2 news: title and hot display it as list
            if not b2:
                time = time + datetime.timedelta(-1)
            else:
                break
        for news_list in b2['hot']:
            news_title = news_list[0]
            news_heat = news_list[1]
            dic[news_title] = news_heat
    return render_template('news/newslist.html', dic=dic, news_time=time_str)


@news.route('/wordcloud/<news_title>')
def wordcloud(news_title):
    if current_user.is_authenticated:
        dic = emotion_db.C1.find_one({'user':current_user.username})
        if not dic:
            dic = {'user':current_user.username,'news':{},'wbtopic':{},'wbhot':{}}
        if today not in dic['news']:
            dic['news'][today] = []
        dic['news'][today].append(news_title)
        emotion_db.C1.save(dic)

    b1 = emotion_db.B1.find_one({'title': news_title})
    if not b1:
        return redirect(url_for('main.index'))
    dic = b1['words']
    content = b1['content']
    time_str = b1['time'][:10].replace('-', '')
    od = OrderedDict(sorted(dic.iteritems(), key=lambda d: d[1], reverse=True))
    emotion = [0, 0, 0, 0]
    comments = []
    if len(od) > 16:
        k = 0
        dic = {}
        for i in od:
            dic[i] = od[i]
            k = k + 1
            if k > 16:
                od = dic
                break

    b3 = emotion_db.B3.find_one({'title': news_title})
    if b3:
        emotion = b3['score']
        comments = b3['comment']

    li = []
    b4 = emotion_db.B4.find_one({'title': news_title})
    if b4:
        for l in b4['related']:
            li.append(l)
        li.sort(key=lambda l: l[2], reverse=True)
        if len(li)>15:
            li = li[0:15]
    return render_template('news/wordcloud.html', dic=json.dumps(od), emotion=emotion, comments=comments, news_title=news_title, content=content, li=li, time_str=time_str)
