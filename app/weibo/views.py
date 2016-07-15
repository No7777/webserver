from flask import render_template, session, request, redirect, url_for
import sys
import json
from collections import OrderedDict
from . import weibo
from .. import emotion_db
import datetime
from flask.ext.login import current_user
reload(sys)
sys.setdefaultencoding('utf8')
today = datetime.date.today()
today = str(today)[0:4]+str(today)[5:7]+str(today)[8:10]

@weibo.route('/weibo')
def weibo_home():
    return render_template('weibo/weibo_home.html')


@weibo.route('/top50', methods=['POST', 'GET'])
def top50():
    time = datetime.datetime.now()
    dic = {}
    if request.method == 'POST':
        time_str = request.form['time'].replace('-', '')
        session['top50_time'] = time_str
        return redirect(url_for('weibo.top50'))
    if 'top50_time' in session:
        time_str = session['top50_time']
        a3 = emotion_db.A3.find_one({'time': str(time_str)})
        if not a3:
            del session['top50_time']
            return 'Not Found'
        for key, value in a3['top'].items():
            for i in value:
                dic[i[0]] = int(i[1])
        od = OrderedDict(sorted(dic.iteritems(), key=lambda d: d[1], reverse=False))
    else:
        while True:
            time_str = str(time)[:10].replace('-', '')
            a3 = emotion_db.A3.find_one({'time': str(time_str)})
            if not a3:
                time = time + datetime.timedelta(-10)
            else:
                break
        for key, value in a3['top'].items():
            for i in value:
                dic[i[0]] = int(i[1])
        od = OrderedDict(sorted(dic.iteritems(), key=lambda d: d[1], reverse=False))
    return render_template('weibo/top50.html', dic=json.dumps(od), time=time_str)


@weibo.route('/trend/<topic>')
def trend(topic):
    if current_user.is_authenticated:
        dic = emotion_db.C1.find_one({'user':current_user.username})
        if not dic:
            dic = {'user':current_user.username,'news':{},'wbtopic':{},'wbhot':{}}
        if today not in dic['wbhot']:
            dic['wbhot'][today] = []
        dic['wbhot'][today].append(topic)
        emotion_db.C1.save(dic)

    a4 = emotion_db.A4.find_one({'topic': topic})
    dic = {}
    time = []
    rank = []
    index = []
    for l in a4['history']:
        time.append(l[0])
        rank.append(l[2])
        index.append(l[1])
    dic['time'] = time
    dic['index'] = index
    dic['rank'] = rank
    a5 = emotion_db.A5.find_one({'topic': topic})
    if not a5:
        a5 = {'content': []}
    return render_template('weibo/trend.html', dic=json.dumps(dic),topic=topic, li=a5['content'])


@weibo.route('/topic', methods=['GET', 'POST'])
def topic():
    time = None
    dic = {}
    if request.method == 'POST':
        time_str = request.form['time'].replace('-', '')
        session['topic_time'] = time_str
        return redirect(url_for('weibo.topic'))

    if 'topic_time' in session:
        time_str = session['topic_time']
        a1 = emotion_db.A1.find_one({'time': time_str})
        if not a1:
            del session['topic_time']
            return 'Not Found'
        for key, value in a1['category'].items():
            dic[key] = value[2]
    else:
        time = datetime.datetime.now()
        while True:
            time_str = str(time)[:10].replace('-', '')
            a1 = emotion_db.A1.find_one({'time': str(time_str)})
            if not a1:
                time = time + datetime.timedelta(-1)
            else:
                break
        for key, value in a1['category'].items():
            dic[key] = value[2]
    return render_template('weibo/topic.html', dic=dic, weibo_time=time_str)


@weibo.route('/weibolist/<time>/<category>')
def weibolist(time, category):
    a1 = emotion_db.A1.find_one({'time': time})
    li = []
    for key in a1['category'][category][1]:
        li.append(key)
    return render_template('weibo/weibolist.html', li=li, category=category)


@weibo.route('/topicdisplay/<topic_name>')
def topicdisplay(topic_name):
    if current_user.is_authenticated:
        dic = emotion_db.C1.find_one({'user':current_user.username})
        if not dic:
            dic = {'user':current_user.username,'news':{},'wbtopic':{},'wbhot':{}}
        if today not in dic['wbtopic']:
            dic['wbtopic'][today] = []
        dic['wbtopic'][today].append(topic_name)
        emotion_db.C1.save(dic)

    dic = {}
    time = []
    read = []
    click = []
    a2 = emotion_db.A2.find_one({'topic': topic_name})
    if not a2:
        return 'Not Found'
    content = a2['content']
    topic = a2['topic']
    for li in a2['history']:
        time.append(li[0])
        read.append(li[1])
        click.append(li[2])
    dic['time'] = time
    dic['read'] = read
    dic['click'] = click
    return render_template('weibo/topicdisplay.html', dic=json.dumps(dic), content=content, topic=topic)

