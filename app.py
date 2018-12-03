from flask import Flask, render_template, request, redirect, url_for
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

service = NaturalLanguageUnderstandingV1(
version='2018-03-16',
url='https://gateway.watsonplatform.net/natural-language-understanding/api',
iam_apikey='p-qstDcxg9kZ_7VqXOyUiCYhCE97ftQV8xqJ5_VfO8Gu')

def get_keywords(content):
    response = service.analyze(
    text=content,
    features=Features(entities=EntitiesOptions(),
                      keywords=KeywordsOptions())).get_result()

    kword_list = [keyword["text"] for keyword in response["keywords"]]
    return json.dumps(kword_list)

app = Flask(__name__)
blog = { 
    'name': 'My awesome blog ',
    'posts': {}
       
    
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/post/<int:post_id>') # /post/2

def post(post_id):
    post = blog['posts'].get(post_id)

    
    if not post:
        return render_template('404.jinja2', message='A post was not found.')

    return render_template('post.jinja2', post=post)

@app.route('/post/<int:post_id>/like') # /post/2/like
def like(post_id):
    post = blog['posts'].get(post_id)
    if not post:
        return render_template('404.jinja2', message='A post was not found.')
    if request.method == 'POST' :
        post.likes += 1
        #blog['posts'][post.id] = post
        print('LIKED PPOST')
        return redirect(url_for('post', post_id=post_id))

    

    return render_template('post.jinja2', post=post)



@app.route('/post/create', methods=['GET', 'POST'])

def create():
    if request.method == 'POST' :
       title = request.form.get('title')
       content = request.form.get('content')
       keywords = get_keywords(content)
       post_id = len(blog['posts']) #to store in dictionary 
       blog['posts'][post_id] = {'post_id': post_id, 'title': title, 'content': content, 'keywords': keywords, 'likes': 0}
       return redirect(url_for('post', post_id=post_id))
    return render_template('create.html')

app.run()
