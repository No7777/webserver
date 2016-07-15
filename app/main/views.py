from flask import render_template
from . import main
from flask.ext.login import current_user
import recommend


@main.route('/')
def index():
    if current_user.is_authenticated:
        username = current_user.username
        news = recommend.newsRecommend(username)
        news_list = news.run()
        wbtopic = recommend.wbtopicRecommend(username)
        wbtopic_list = wbtopic.run()
        wbhot = recommend.wbhotRecommend(username)
        wbhot_list = wbhot.run()
        return render_template('main/index.html', news_list=news_list, wbtopic_list=wbtopic_list, wbhot_list=wbhot_list)
    return render_template('main/index.html')
