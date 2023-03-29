import os
import numpy as np

def main_routine():
    num_sub_events = int(float(input("How many subevents do you have? ")))
    arr = input("Input tuples of subevent odds and complement subevent odds. ") 
    l = list(map(int,arr.split(' '))) 
    
    subevent_array = np.array(l).reshape(num_sub_events, 2)
    vig = np.empty((num_sub_events, 1))
    subevent_complement_prob = np.empty((num_sub_events, 2))
    
    vig, subevent_complement_prob = calculate_vig(subevent_array)
    
    actual_probs = calculate_actual_probs(subevent_complement_prob, vig)
    
    interesection_q = int(input("Input 1 if you want to take the intersection of all your subevents. Input 0 otherwise."))
    
    if intersection_q ==1:
        true_probability = intersect_subevent_prob(actual_probs)
    else:
        print("Functionality to take the union of several subevents is currently not supported.")
        
        
    print(f"The true probability of all subevents occurring simultaneously is {np.round(true_probability*100,1)}%. ")
    
    br_amt = float(input("What is your bankroll amount?))
    odds_offered = int(input("What odds are you considering betting on?")
    boosted = int(input("Is this part of a boosted bet offering? Answer 1 for yes, 0 for no."))
    if boosted ==1:
        boosted = True
    else:
        boosted = 0
   
    prop, dol = kelly_bet_percentage(true_probability, odds_offered, br_amt, boosted)
    if boosted:
        place = ""
    else: 
        place = "not"          
    print(f"Our calculations say that, for the example event with given odds, you should bet ${np.round(dol,2):,}, given you have a bankroll amount of ${br_amt:,}. Note: this assumes that the boost maximum of $50 is{place} in effect. ")
    ev = compute_ev(true_probability, odds_offered)
    print(f"So, expect {ev}% return on each dollar bet on this offer. ")
                       
def calculate_vig(subevent_array): 
    for i in range(0, num_sub_events):
        if subevent_array[i][0] > 0: # 1st column, i.e. subevent odds
            subevent_complement_prob[i][0] = 100/(subevent_array[i][0]+100)
        else: 
            subevent_complement_prob[i][0] = abs(subevent_array[i][0]) / (abs(subevent_array[i][0]) + 100)
        if subevent_array[i][1] > 0: #2nd column, i.e. complement subevent odds
            subevent_complement_prob[i][1] = 100/(subevent_array[i][1]+100)
        else: 
            subevent_complement_prob[i][1] = abs(subevent_array[i][1]) / (abs(subevent_array[i][1]) + 100)
        vig[i][0] =  subevent_complement_prob[i][0]+ subevent_complement_prob[i][1]-1
    
    return vig, subevent_complement_prob

    
def calculate_actual_probs(subevent_complement_prob, vig):
    actual_probs = np.empty((num_sub_events, 2))
    for i in range(num_sub_events):
        actual_probs[i] = np.divide(subevent_complement_prob[i],1+vig[i])
    return actual_probs

def intersect_subevent_prob(actual_probs):
    """
   Input the matrix with shape (number of sub events, 2) that contains true probabilities for each event. 
    Assumes the subevents are independent. 
    Outputs the probability of all subevents occurring simultaneously. 
    """
    intersection_prob = np.empty((1,2))
    intersection_prob = np.prod(actual_probs, axis = 0)
    return intersection_prob[0]

def calculate_fair_odds(true_probability):
    """
    Input: true_probability should be a float between 0 and 1.
    Output: Fair odds on the usual betting scale (100+ representing unlikely events, -100- representing likely events)
    """
    if true_probability <= .5:
        true_odds = 100/true_probability -100
    elif true_probability > .5 and true_probability <= 1:
        true_odds = -100/(1-true_probability)+100
    else:
        "Invalid input probability"
    return true_odds


def kelly_bet_percentage(true_probability, odds_offered, bankroll_amt, boost_bet = True):
    """
    Input the true probability (estimated) of the main event happening. Input the odds offered you by the sportsbook. 
    Input the dollar value of your betting bankroll.
    Output the proportion of the bankroll you should risk (maximum $50 if this is a boosted bet). If 0 is the output, this means don't bet. 
    Output the dollar amount you should risk. 
    
    NB: kelly formula is f = p - (1-p)/b, where p is true probability, b is the proportion of each dollar bet that you would gain with a win. 
    e.g. if the odds offered are +200, you will win 2.0 dollars for every dollar bet. If the odds offered are -400, you win .25 for every dollar bet. 
    """
    
    if odds_offered > 0: 
        b_value = odds_offered/100
    else:
        b_value = 100/abs(odds_offered)
    
    kelly_proportion = true_probability - (1-true_probability)/b_value
    if kelly_proportion >=0 and boost_bet ==True:
        dollar_value_to_bet = min(kelly_proportion*bankroll_amt, 50)
    elif kelly_proportion >= 0 and boost_bet == False:
        dollar_value_to_bet = kelly_proportion*bankroll_amt
    else: 
        print("Don't bet on this!")
        dollar_value_to_bet =0 
    
    return kelly_proportion, dollar_value_to_bet
        
def compute_ev(true_probability, given_odds):
    fair_odds = calculate_fair_odds(true_probability)
    if fair_odds >0 and given_odds > 0:
        ev = true_probability* (given_odds - fair_odds)
    elif fair_odds > 0 and given_odds < 0:
        ev = true_probability*(10000/abs(given_odds) - fair_odds)
        print("Don't bet on this!")
    elif fair_odds < 0 and given_odds < 0:
        ev = true_probability* (given_odds - fair_odds)
    elif fair_odds <0 and given_odds >0:
        ev = true_probability*(given_odds - 10000/abs(fair_odds))
    else: 
        print("Don't bet on this!")
    return np.round(ev,1)
    