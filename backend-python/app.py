# -*- coding: utf-8 -*-
"""
Main application entry point for the Flask web server.
"""
from flask import Flask, render_template, request, jsonify
from neo_db.query_graph import query, get_KGQA_answer, get_answer_profile
from kgqa.ltp import get_target_array

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(name=None):
    """
    Render the home page.
    """
    return render_template('index.html', name=name)

@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    Render the search page.
    """
    return render_template('search.html')

@app.route('/KGQA', methods=['GET', 'POST'])
def KGQA():
    """
    Render the KGQA page.
    """
    return render_template('KGQA.html')

@app.route('/get_profile', methods=['GET', 'POST'])
def get_profile():
    """
    API to get character profile.
    """
    name = request.args.get('character_name')
    json_data = get_answer_profile(name)
    return jsonify(json_data)

@app.route('/KGQA_answer', methods=['GET', 'POST'])
def kgqa_answer():
    """
    API to get answer for a question.
    """
    question = request.args.get('name')
    target_words = get_target_array(str(question))
    json_data = get_KGQA_answer(target_words)
    return jsonify(json_data)

@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    """
    API to search for a character's relations.
    """
    name = request.args.get('name')
    json_data = query(str(name))
    return jsonify(json_data)

@app.route('/get_all_relation', methods=['GET', 'POST'])
def get_all_relation():
    """
    Render the all relation page.
    """
    return render_template('all_relation.html')

if __name__ == '__main__':
    # Debug mode should be False in production
    app.debug = True
    app.run()
