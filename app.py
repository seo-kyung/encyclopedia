import sys
import time
import logging
import random
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import time
import markovify
import os
import json
import signal
from tqdm import tqdm
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

dataDir = "data"

emotions = ["joy", "sadness", "anger", "surprise"]
models = {}


@app.route('/')
def root():
    session['emotion'] = ''
    args = {}
    d0 = date(2020, 8, 27)
    now = date.today()
    delta = now - d0
    args["days"] = (delta.days)

    args["total"] = 0
    for emotion in emotions:
        with open(os.path.join(dataDir, f"{emotion}.json"), 'rt') as f:
            try:
                entries = json.load(f)
                args[emotion] = len(entries.keys())
                args["total"] += args[emotion]
            except ValueError:
                args[emotion] = 0
                print(f"Could not retrieve data file for {emotion}.")

    return render_template('main.html', **args)


def renderEmotion(emotion):
    session['emotion'] = emotion
    with open(os.path.join(dataDir, f"{emotion}.json"), 'rt') as f:
        try:
            entries = json.load(f)
            count = len(entries.keys())
        except ValueError:
            count = 0
            print(f"Could not retrieve data file for {emotion}.")

    corpus = [(v['message'], f"{v['name']}, {v['title']}", str(k))
              for k, v in entries.items()]
    return render_template(f'{emotion}.html', count=count, corpus=corpus)


@app.route('/joy')
def renderJoy():
    return renderEmotion('joy')


@app.route('/sadness')
def renderSadness():
    return renderEmotion('sadness')


@app.route('/anger')
def renderAnger():
    return renderEmotion('anger')


@app.route('/surprise')
def renderSurprise():
    return renderEmotion('surprise')


@app.route('/output')
def output():
    return render_template('output.html', sentence="Welcome.", emoji=url_for('static', filename='assets/img/emoji/neutral.svg'))


@app.route("/getEmoji.json")
def getEmoji():
    emotion = session['emotion']
    if session['emotion'] in emotions:
        return url_for('static', filename=f'assets/img/emoji/{emotion}.svg')
    else:
        return url_for('static', filename='assets/img/emoji/neutral.svg')

@app.route("/getSentence.json")
def getSentence():
    if session['emotion'] in models:
        sentence = models[session['emotion']].make_sentence(tries=20)
        if sentence is not None:
            return (str(sentence))
        else:
            return "Please enter an additional sentence."
    else:
        return "Please select an emotion."


@app.route('/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({"success": True, "message": "Server is shutting down..."})


def rebuild_model(emotion, corpus):
    print(f"Building model for {emotion}...")
    models[emotion] = markovify.Text(corpus)


@app.route('/entry', methods=['POST', 'DELETE'])
def entry():
    if request.method == 'POST':
        now = str(datetime.now())
        entry = {}
        entry[now] = {}
        entry[now]['message'] = request.form['message']
        entry[now]['name'] = request.form['name']
        entry[now]['title'] = request.form['title']
        emotion = session['emotion']
        fname = f'data/{emotion}.json'
        with open(fname, 'rt') as f:
            try:
                entries = json.load(f)
            except ValueError:
                entries = {}
            entries.update(entry)

        with open(fname, "wt") as f:
            json.dump(entries, f, indent=2)

        newMessages = [v['message'] for k, v in entries.items()]
        rebuild_model(emotion, newMessages)
        return redirect(url_for(f'render{emotion.capitalize()}'))
    elif request.method == 'DELETE':
        timestamp = request.form['timestamp']
        emotion = session['emotion']
        fname = f'data/{emotion}.json'
        with open(fname, 'rt') as f:
            try:
                entries = json.load(f)
            except ValueError:
                entries = {}
            entries.pop(timestamp)

        with open(fname, "wt") as f:
            json.dump(entries, f, indent=2)
        return jsonify(isError=False,
                       message=f"Deleted entry with timestamp {timestamp}",
                       statusCode=200), 200


for emotion in emotions:
    with open(os.path.join(dataDir, f"{emotion}.json"), 'rt') as f:
        try:
            entries = json.load(f)
            messages = [v['message'] for k, v in entries.items()]
            rebuild_model(emotion, messages)
        except ValueError:
            print(f"Could not build model for {emotion}.")


# for emotion in emotions:
#     with open(f'data/{emotion}.txt') as f:
#         for line in f:
#             now = str(datetime.now())
#             entry = {}
#             entry[now] = {}
#             entry[now]['message'] = line
#             entry[now]['name'] = 'Unknown'
#             entry[now]['title'] = 'Unknown'
#             fname = f'data/{emotion}.json'
#             with open(fname, 'rt') as f:
#                 try:
#                     entries = json.load(f)
#                 except ValueError:
#                     entries = {}
#                 entries.update(entry)

#             with open(fname, "wt") as f:
#                 json.dump(entries, f, indent=2)
