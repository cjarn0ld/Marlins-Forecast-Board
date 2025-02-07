import numpy as np

def brier_score(probability, actual):
    """Calculate Brier score for a single forecast"""
    return (probability - actual) ** 2

def accuracy_score(probability, actual):
    """Calculate accuracy based on forecast probability"""
    return 1 - abs(probability - actual)

def calculate_user_scores(user_forecasts, outcomes):
    """
    Calculate overall scores for a user across all questions
    
    :param user_forecasts: List of user's forecasts
    :param outcomes: Dictionary of question outcomes
    :return: Dictionary with user's scores
    """
    brier_scores = []
    accuracy_scores = []
    
    for forecast in user_forecasts:
        question_id = forecast.question_id
        if question_id in outcomes:
            actual = outcomes[question_id]
            brier_scores.append(brier_score(forecast.probability, actual))
            accuracy_scores.append(accuracy_score(forecast.probability, actual))
    
    return {
        'avg_brier_score': np.mean(brier_scores) if brier_scores else None,
        'avg_accuracy': np.mean(accuracy_scores) if accuracy_scores else None
    }