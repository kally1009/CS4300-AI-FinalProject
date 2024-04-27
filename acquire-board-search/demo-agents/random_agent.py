import random 

def agent_function(env, agent):
    observation, reward, termination, truncation, info = env.last()
    if termination or truncation:
        action = None
    else:
        hands = observation["hands"]
        cur_agent = observation["current"] 
        hands = hands.tolist()
        choice = random.sample(hands[cur_agent],1)
        print("choice made",choice)
        action = choice[0]

    return action