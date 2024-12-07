import numpy as np

def calculate_team_score(team_data):
    '''
    Calculates a performance score for a sports team based on win rate, goal difference, and last five match results

    The score is a weighted sum of their:
        - Win rate: ratio of Wins (W) to Matches Played (MP)
        - Goal Difference: Difference between Goals scored (GF) and Goals conceded (GA)
        - Recent form: a recency-weighted score of their recent form, based on a string of the form 'x x x x x'
            - Each 'x' corresponds to a 'W', 'D' or 'L'

    Input: team_data, a dictionary with keys:
        'W' (number of wins),
        'D' (number of draws),
        'L' (number of losses),
        'GF' (number of goals scored)
        'GA' (number of goals allowed)
        'Last 5' (string of results of last 5 matches)

    Output: score: performance score representing the team's strength and recent form
    '''
    win_rate = team_data.get('W', 0) / team_data.get('MP', 1)
    goal_diff = team_data.get('GF', 0) - team_data.get('GA', 0)
    form_values = {'W': 1, 'D': 0.5, 'L': 0}
    form_matches = team_data.get('Last 5', 'D D D D D').split(' ')
    recency_weights = np.array([5, 4, 3, 2, 1])
    form_strength = sum(form_values.get(match, 0) * weight for match, weight in zip(form_matches, recency_weights)) / sum(recency_weights)
    score = (0.4 * win_rate) + (0.3 * goal_diff) + (0.2 * form_strength)
    return score

def logistic(x):
    '''
    Defines a logistic function to assist in the normalization of the match probabilities

    Input: x, used as the team score from calculate_team_score

    Output: Computed logistical values between 0 and 1
    '''
    return 1 / (1 + np.exp(-x))

def return_probabilities(team_a_score, team_b_score):
    '''
    Calculates and returns the probabilities of Team A winning, Team B winning, and a draw based on their scores.
    The function uses the logistic functions to get normalized scores, computes a draw probability,
    and scale to get probabilities

    Input: team_a_score: performance score representing the team's strength and recent form for team a
    Input: team_b_score: performance score representing the team's strength and recent form for team b

    Output: a 3-Tuple containing the percentage probability of Team A winning, Team B winning, and a Draw
    '''
    team_a_normalized = logistic(team_a_score)
    team_b_normalized = logistic(team_b_score)
    draw_factor = min(team_a_normalized, team_b_normalized) * 0.4
    total_prob = team_a_normalized + team_b_normalized + draw_factor
    prob_team_a = team_a_normalized / total_prob
    prob_team_b = team_b_normalized / total_prob
    prob_draw = draw_factor / total_prob
    return (f"{prob_team_a:.2%}", f"{prob_team_b:.2%}", f"{prob_draw:.2%}")