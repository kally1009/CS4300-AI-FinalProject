import acquire_board_search
import acquire_board_search.envs.acquire_board_search_model as acquire_model
import copy
import random
import numpy as np


INFINITY = 1.e10


max_depth = 4



def EVALUATE(s): #evaluates the whole state. 
    if s.game_over():
        return 6
    player_1_current_score = 0
    player_2_current_score = 0
    current_hotels = s.current_hotels
    for hotel in current_hotels:
        total_tiles = hotel.GET_SIZE()
        weight = hotel.GET_RATING()
        total_hotel_score = total_tiles*weight
        player = hotel.GET_PLAYER_OWNER()
        if player==0:
            player_1_current_score+=total_hotel_score
        else:
            player_2_current_score+=total_hotel_score
    
    #somehow check stand alone tiles

    if s.current_agent == 0:
        if player_1_current_score>=player_2_current_score:
            return 4
        elif player_2_current_score>player_1_current_score:
            return 2

    elif s.current_agent == 1:
        if player_1_current_score>=player_2_current_score:
            return 2
        elif player_2_current_score>player_1_current_score:
            return 4

    

def MAX(s,d):
    if d>= max_depth or s.game_over():
        return EVALUATE(s),None
    vmax = -INFINITY
    best_action = 0
    for a in ACTIONS(s):
        s_prime = RESULT(s,a)
        v,_ = MIN(s_prime,d+1)
        if v > vmax:
            vmax = v
            best_action = a
    return (vmax,best_action) 

def MIN(s,d):
    if d>= max_depth or s.game_over(): #max_depth is a global
        return (EVALUATE(s),None)
    vmin = INFINITY
    best_action = 0
    for a in ACTIONS(s):
        prime_s = RESULT(s,a) #keep track of whose turn it is?
        v,_ = MAX(prime_s,d+1)
        if v < vmin:
            vmin = v
            best_action = a

    return (vmin,best_action)

def ACTIONS(s,player): #need to fix this function
    return s.hands[player] #hands or legal moves?

def RESULT(s,a):
    env = copy.deepcopy(s)
    env.step(a)
    return env



def agent_function(env, agent):
    observation, reward, termination, truncation, info = env.last() #do I need to use the observation?
    
    hands = observation["hands"]
    cur_agent = observation["current"] 
    hands = hands.tolist()
    deck = observation["deck"]
    deck = deck.tolist()
    board = observation["board"]
    board = board.tolist()


    if termination or truncation:
        action = None
    else:
        action = None
        max_eval = 0
        searchable_env = acquire_model.AcquireBoardModel()
        searchable_env.copy_from_env(env)
        env1 = copy.deepcopy(searchable_env)
        evaluation,best_action = MAX(env1,0)
        if env1.game_over():                             
            action = best_action
        else:
            if evaluation>=max_eval:
                max_eval = evaluation
                action = best_action

            
        if action is None:
            action = random.choice(searchable_env.legal_moves())
    return action