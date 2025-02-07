# utils/data_helpers.py
import os
import json
import csv
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def load_questions():
    questions_file = os.path.join(DATA_DIR, 'questions.json')
    with open(questions_file, 'r') as f:
        return json.load(f)

def save_question(question_data):
    questions_file = os.path.join(DATA_DIR, 'questions.json')
    questions = load_questions()
    questions.append(question_data)
    with open(questions_file, 'w') as f:
        json.dump(questions, f, indent=2)

def get_leaderboard():
    responses_file = os.path.join(DATA_DIR, 'responses.csv')
    outcomes_file = os.path.join(DATA_DIR, 'outcomes.csv')
    
    outcomes = {}
    if os.path.exists(outcomes_file):
        with open(outcomes_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                outcomes[int(row['question_id'])] = float(row['actual'])
    
    scores = {}
    if os.path.exists(responses_file):
        with open(responses_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                user = row['user_id']
                if user not in scores:
                    scores[user] = {'questions': 0, 'total_brier': 0}
                
                qid = int(row['question_id'])
                if qid in outcomes:
                    scores[user]['questions'] += 1
                    brier = (float(row['guess']) - outcomes[qid]) ** 2
                    scores[user]['total_brier'] += brier

    rankings = []
    for user, data in scores.items():
        if data['questions'] > 0:
            avg_brier = data['total_brier'] / data['questions']
            rankings.append({
                'user': user,
                'questions': data['questions'],
                'avg_brier': avg_brier,
                'accuracy': 1 - avg_brier
            })
            
    rankings.sort(key=lambda x: x['avg_brier'])
    return rankings