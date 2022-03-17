# Launch with
#
# gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc

from flask import Flask, render_template
from doc2vec import *
import sys

app = Flask(__name__)

@app.route("/")
def articles():
    """Show a list of article titles"""
    article_lst = [[art[0].split('/')[-2], art[0].split('/')[-1],art[1]] for art in articles]
    return render_template('articles.html', articles=article_lst)


@app.route("/article/<topic>/<filename>")
def article(topic,filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    url = topic + '/' + filename
    for art in articles:
        if url == '/'.join(art[0].split('/')[-2:]):
            article_select = art
    article_recommend = recommended(article_select, articles, 5)
    article_reco = [[art[0].split('/')[-2], art[0].split('/')[-1], art[1]] for art in article_recommend]
    return render_template('article.html', article=article_select, articles_reco=article_reco)

# initialization
#i = sys.argv.index('server:app') #For gunicorn
i = sys.argv.index('server.py') #For Flask
glove_filename = sys.argv[i+1]
articles_dirname = sys.argv[i+2]

gloves = load_glove(glove_filename)
articles = load_articles(articles_dirname, gloves)

if __name__ == "__main__":
    app.run()
