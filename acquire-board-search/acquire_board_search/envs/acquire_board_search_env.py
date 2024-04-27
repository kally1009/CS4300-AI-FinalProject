import gymnasium
import numpy as np
import copy
import random
from gymnasium import spaces
from acquire_board_search.envs.acquire_board_search_model import AcquireBoardModel
from acquire_board_search.envs.acquire_board_search_model import AcquireBoardState


from pettingzoo import AECEnv
from pettingzoo.utils import wrappers
from pettingzoo.utils.agent_selector import agent_selector
#index = ((row*12)+(col%12)) calculate index into the board/unwrap to get col and row. 

def env(render_mode=None):
    internal_render_mode = render_mode
    env = raw_env(render_mode=internal_render_mode)
    env = wrappers.TerminateIllegalWrapper(env)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


class raw_env (AECEnv):
    metadata = {
        "render_modes": ["human","ascii"], #the only representation will be in terminal. Human and ascii are the same.
        "name": "aquire_board_search_v0",
        "is_parallelizable" : False,
    }

    def __init__(self,render_mode=None):
        # 9 rows x 12 columns
        # blank space = 0
        # agent 0 -- 1
        # agent 1 -- 2

        self.render_mode = render_mode
        self.board = [0] * (9 * 12)
        self.agents = ["player_0","player_1"]
        self.possible_agents = self.agents[:]
        self.terminations = None
        self.winner = -1
        self.current_agent = 0
        self.game = AcquireBoardState()
        self.hand = [[],[]] #The MOVES available for each agent. Will need to consistently update this after each step. 
        self.deck = []
        
        
        self.action_space = {i: spaces.Discrete(107) for i in range (len(self.agents))} #108 is 12*9. 107 is up to but not including the last space.
        self.observation_space = {
            i: spaces.Dict(
                {
                    "board" : spaces.Box(
                        low=0, high=1, shape = (9,12), dtype=np.int8
                    ),
                    "hands": spaces.Box(low=0,high=107,shape=(2,6),dtype=np.int8),
                    "deck" : spaces.Box(low=-1,high=107,shape=(107,),dtype=np.int8),
                    "current": spaces.Box(low=0,high=1,shape=(1,),dtype=np.int8)
                }
            )
            for i in self.agents
        }

    def observe(self, agent): 
        board_vals = np.array(self.board,dtype=np.int8)
        cur_player = self.possible_agents.index(agent)
        hands_tiles = np.array(self.hand,dtype=np.int8)
        cur_deck = np.array(self.deck,dtype=np.int8)
        

        return {"board":board_vals, "hands":hands_tiles,"deck":cur_deck,"current":cur_player} 

    def reset(self, seed=None, options=None):
        self.board = [0] * (9* 12)
        self.agents = self.possible_agents[:]
        self.rewards = {i: 0 for i in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {i: {} for i in self.agents}
        self.game = AcquireBoardState()
        self._agent_selector = agent_selector(self.agents)

        self.agent_selection = self._agent_selector.reset()
        starting_hand = self.game.start_game()
        self.hand = starting_hand
        self.deck = self.game.deck
        

    def step(self,action): 
        #action is the tile grid position
        if (
            self.terminations[self.agent_selection]
            or self.truncations[self.agent_selection]
        ):
            self._was_dead_step(action)
            return
        
        player = self.agents.index(self.agent_selection)
        hand = self.game.turn(action,player) 
        self.hand[player] = hand #updating the player hand
        updated_invalid_list = self.game.return_invalid_tile_list()
        piece = self.current_agent + 1
        self.update_board(action,piece)

        for invalid_space in updated_invalid_list:
            self.update_board(invalid_space,3) #3 represents invalid spaces

        next_agent = self._agent_selector.next()
        winner = self.check_for_winner()
        if winner:
            print("The winner is Player",self.winner)


        

        winner = self.check_for_winner()

        if winner:
            self.rewards[self.agent_selection]+=1
            self.rewards[next_agent]-= 1
            self.terminations = {i: True for i in self.agents}
        self.agent_selection = next_agent
        self.current_agent = ((self.current_agent+1)%2)
        self._accumulate_rewards() #Figure this out with the rewards?
        
        if self.render_mode == "ascii" or self.render_mode=="human":
            self.render()
        
        
    def render(self): 
        if self.render_mode is None:
            gymnasium.logger.warn(
                "You are calling render method without specifying any render mode."
            )
            return
        if self.render_mode == "ansi" or self.render_mode=="human":
            self.print_board()
            return
        
    def print_board(self):
        s = ""
        s += "+" + "---+"*12
        for row in range(9):
            line = "|"
            for col in range(12):
                i = row*12+col
                c = " {} |".format(self.board[i])
                line += c
            s += "\n" + line
            s += "\n" + "+" + "---+"*12
        print(s)
        return s
    
    def update_board(self,action,piece): #an action is the calculated index of the grid posision
        if self.board[action]!=piece:
            self.board[action] = piece           



    def observation_space(self,agent):
        return self.observation_space[agent]

    
    def action_space(self,agent):
        return self.action_spaces[agent]
    
    def _legal_moves(self):
        legal_moves = []
        for i in range(12):
            if self.board[i]==0:
                legal_moves.append(i)
            for j in range(9):
                if self.board[j]==0:
                    legal_moves.append(j)

        return legal_moves
    
    def check_for_winner(self):
        if self.game.GAME_OVER():
            self.winner = self.game.end_game()
            return True
        else:
            return False
