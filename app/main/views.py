from flask import render_template, request, session, redirect, url_for, abort
from . import main
from flask.ext.login import current_user
import recommend
from search import search


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


@main.route('/search', methods=['GET', 'POST'])
def search_keyword():
    if request.method == 'POST':
        keyword = request.form['keyword']
        session['keyword'] = keyword
        return redirect(url_for('main.search_keyword'))
    if 'keyword' not in session:
        abort(404)
    se = search(session['keyword'])
    se.run()
    news_list = se.news
    wbtopic_list = se.wbtopic
    wbhot_list = se.wbhot
    return render_template('main/search.html', news_list=news_list, wbtopic_list=wbtopic_list, wbhot_list=wbhot_list)
