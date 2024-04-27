import acquire_board_search
import acquire_board_search.envs.acquire_board_search_model as acquire_model

import time
import random_agent

def main():
    agent_function = {"player_0": random_agent.agent_function, "player_1": random_agent.agent_function}
    times = {"player_0": 0.0, "player_1":0.0}



    env = acquire_board_search.raw_env(render_mode="human")
    env.reset()

    for agent in env.agent_iter():
        if True:
            env1 = acquire_model.AcquireBoardModel()
            env1.copy_from_env(env)

            t1 = time.time()
            action = agent_function[agent](env,agent)
            t2 = time.time()
            times[agent]+= (t2-t1)
            
            env.step(action)
            try:
                observation, reward, termination, truncation, info = env.last()
                print("{} took action {}".format(agent, action))
                if termination or truncation:
                    if len(env.rewards.keys()) == 2:
                        winner = None
                        for a in env.rewards:
                            if env.rewards[a] == 1:
                                winner = a
                                break
                        if winner is not None:
                            print(f"{winner} wins.")
                        else:
                            print("Not sure who won.")
                        if True:
                            """text display of board"""
                            env1 = acquire_model.AcquireBoardModel()
                            env1.copy_from_env(env)
                        break
            except:
                pass

    env.close()

    for agent in times:
        print(f"{agent} took {times[agent]:8.5f} seconds.")
    return
        
if __name__ == "__main__":
    if False:
        import cProfile
        cProfile.run('main()')
    else:
        main()



'''
Questions:
- How to import from other files again?

- Action Mask

- Observation Space. I want to return the hand and of course the current state of the board. 

- How to connect with the agents... should I do the play.py like adversarial search? 
- Is the model supposed to help the agents or directly interact with the environment?


'''