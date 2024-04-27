import numpy as np
import copy
import random


class AcquireBoardState:

    def __init__(self):
        self.tiles_drawn = []
        self.tiles_played = []
        self.current_hotels = []
        self.hotel_name_list_and_rank = [("Continential",3), ("Imperial",3), ("American",2), ("Festival",2), ("World Wide",2), ("Luxor",1), ("Tower",1)]
        self.total_num_tiles = 107
        self.hand = [[],[]]
        self.deck = []
        self.invalid_tile_space = [] #list of tuples of tile grid positions
        self.board_tiles = [0] * (9*12)

    def tile_valid(self,tile):
        x = tile//12
        y = tile - (x*12)

        for space in self.invalid_tile_space:
            if tile == space:
                return False
        if x>=0 and x<=8:
            if y>=0 and y<=11:
                return True
        return False
    
    def return_invalid_tile_list(self):
        return self.invalid_tile_space
    
    
    def generate_tile(self):
        new_tile = self.deck.pop(0)
        self.deck.append(-1)
        if new_tile==-1:
            return None
        
        return new_tile #returns index position
    

    def generate_tile_name(self,position): #not currently used, but can be in the future.
        alpha_list = ["A","B","C","D","E","F","G","H","I"]
        if self.tile_valid(position):
            x,y = position
            name = alpha_list[x]+"-"+str(y+1)
            print(name)
            return name
        return " - "
        

    def generate_neighbors(self,position): #generate all posisitions around a tile
        x = position[0]
        y = position[1]
        neighbors = [] #list of indexes of the neighbors on the board
        if x>=0 and x<11:
            new_x = x+1
            index = ((new_x*12)+(y%12))
            neighbors.append((index))
        if y>=0 and y<8:
            new_y = y+1
            index = ((x*12)+(new_y%12))
            neighbors.append((index))
        if x<=11 and x>0:
            new_x = x-1
            index = ((new_x*12)+(y%12))
            neighbors.append((index))
        if y<=8 and y>0:
            new_y = y-1
            index = ((x*12)+(new_y%12))
            neighbors.append((index))
        return neighbors
    
    def generate_played_neighbors(self,neighbors): #only generates neighbors that have been played on the board. Filtered.
        played_neighbors = []
        for neighbor in neighbors:
            for j in range(len(self.tiles_played)):
                if neighbor == self.tiles_played[j]:
                    played_neighbors.append(self.tiles_played[j])
        return played_neighbors #returns a filtered list of the played neighbors by index.

    def GAME_OVER(self):
        for hotel in self.current_hotels:
            if hotel.GET_SIZE()>=41:
                return True
        if self.deck[0]==-1:
            return True
        return False


    
    def remove_tile_from_hand(self,player,tile): #tile is the index in the board
        for i in range (len(self.hand[player])):
            if self.hand[player][i]==tile:
                self.hand[player].pop(i)
                return


    def draw(self,player):
        new_tile = self.deck.pop(0) #comes out as the index
        self.deck.append(-1)
        self.hand[player].append(new_tile)
        self.update_tile_drawn_list(new_tile) #index. The tile is an index that needs to be unpacked for use.
        return new_tile

    
    def check_and_update_invalid_spaces(self): #check for new invalid places after each turn.
        check = True
        while check:
            assigned = []
            check=False
            for h in range(len(self.hand)):
                for tile in self.get_player_hand(h):
                    tile_x = tile//12
                    tile_y = tile-(tile_x*12)
                    neighbors = self.generate_neighbors((tile_x,tile_y))
                    for neighbor in neighbors:
                        for hotel in self.current_hotels:
                            lst = self.get_hotel_tile_list(hotel)
                            for tile in lst:
                                if tile==neighbor:
                                    assigned.append(hotel)
                if len(assigned)>1:
                    owner = assigned[0]
                    
                    for i in range(len(assigned)):
                        if i!=0:
                            if assigned[i]!=owner:
                                check=True
                                self.invalid_tile_space.append(tile)
                                _ = self.remove_tile_from_hand(h,tile)
                                self.draw(h)
                                
        return


    def place_tile(self,tile_position,player): 
        
        tile_index = ((tile_position[0]*12)+(tile_position[1]%12))
        neighbors = self.generate_neighbors(tile_position)
        played_neighbors = self.generate_played_neighbors(neighbors)
        self.remove_tile_from_hand(player,tile_index) #returns index
        part_of_hotel = []
        stand_alone = []
        for neighbor in played_neighbors:
            for hotel in self.current_hotels:
                lst = self.get_hotel_tile_list(hotel)
                for tile in lst:
                    if tile==neighbor:
                        part_of_hotel.append((neighbor,hotel))
                    stand_alone.append(neighbor)
            
        if len(part_of_hotel)>1:
            self.invalid_tile_space.append(tile_index)

        if len(part_of_hotel)==1:
            self.add_tile_to_hotel(tile_index,part_of_hotel[0][1])

        
        if len(self.hotel_name_list_and_rank)<=6:
            if len(stand_alone)>=1:
                hotel = self.new_hotel(stand_alone[0],tile_index,player)
                if len(stand_alone)>1:
                    for i in range(1,len(stand_alone)):
                        self.add_tile_to_hotel(stand_alone[i],hotel)

        
        self.tiles_played.append(tile_index)
        self.update_board_tile_list(tile_index,player)

        return

    def update_tile_drawn_list(self,tile):
        self.tiles_drawn.append(tile)


    def update_board_tile_list(self,tile,player):
        self.board_tiles[tile] = player

    def get_updated_board_tile_list(self):
        return self.tiles_played
    
    def get_player_hand(self,player):
        return self.hand[player]
    
    def add_tile_to_hotel(self,tile,hotel):
        hotel.UPDATE_TILE_LIST(tile)

    def new_hotel(self,tile1,tile2,current_player):
        player = current_player
        if len(self.current_hotels)<=6:
            name,rank = self.hotel_name_list_and_rank.pop(0)
            new_hotel = HotelModel(tile1,tile2,name,rank,player)
            self.current_hotels.append(new_hotel)
            return new_hotel
        
    def get_hotel_tile_list(self,hotel):
        return hotel.GET_TILE_LIST()
        
        
    def start_game(self): #init/reset
        deck = list(range(0,108))
        random.shuffle(deck)
        self.deck = copy.deepcopy(deck)

        player1_start_index = self.deck.pop(0)
        player2_start_index = self.deck.pop(0)
        self.deck.append(-1)
        self.deck.append(-1)

        p1_x = (player1_start_index//12)
        p1_y = player1_start_index - (p1_x*12)

        p2_x = (player2_start_index//12)
        p2_y = player2_start_index - (p2_x*12)
        
        p1 = (p1_x,p1_y) #position 
        p2 = (p2_x,p2_y)

        self.place_tile(p1,0)
        self.place_tile(p2,1)
        
        for i in range(6): #start hand of 6 tiles
            self.draw(0)
            self.draw(1)

        return self.hand

    def turn(self,action,player):
        action_x_position = action//12
        action_y_position = action - (action_x_position*12)
        new_action = (action_x_position,action_y_position)
        _ =self.place_tile(new_action,player) #pass in position for place tile
        self.draw(player)
        self.check_and_update_invalid_spaces()
        return self.hand[player]
    
    def end_game(self):
        player_1_score = 0
        player_2_score = 0
        for hotel in self.current_hotels:
            total_tiles = hotel.GET_SIZE()
            weight = hotel.GET_RATING()
            total_score_hotel = total_tiles*weight
            player = hotel.GET_PLAYER_OWNER()
            if player==0:
                player_1_score+=total_score_hotel
            else:
                player_2_score+=total_score_hotel
            
        if player_1_score>player_2_score:
            return 0
        elif player_2_score>player_1_score:
            return 1
        else: #if it's a tie
            return 2

            

class HotelModel:
    def __init__(self,tile1,tile2,name,rating,player):
        #Tiles are represented as a string "A-1", "I-15", etc. List of strings of tiles.
        self.tile_list = [tile1,tile2]
        self.name = name
        self.rating = rating
        self.owner_player = player

    def IS_SAFE(self):
        #returns true or false if number of tiles is greater or equal to 11
        if len(self.tile_list)>=11: 
            return True
        else:
            return False
        
    def UPDATE_TILE_LIST(self,tile):
        self.tile_list.append(tile)
        return
    
    def GET_NAME(self):
        return self.name
    
    def GET_RATING(self):
        return self.rating
    
    def GET_TILE_LIST(self):
        return self.tile_list
    
    def GET_SIZE(self):
        return len(self.tile_list)
    
    def GET_PLAYER_OWNER(self):
        return self.owner_player
    
    def PRICE_PER_STOCK(self):
        #will add stock features later. Will look up in a table depending on rating and number of tiles in hotel chain.
        pass
    def NUM_STOCK(self):
        pass


class AcquireBoardModel: #may take this out or need to get pieces from above class
    def __init__(self):
        
        self.board = [0] * (9 * 12)
        self.agents = ["player_0","player_1"]
        self.possible_agents = self.agents[:]
        self.terminations = None
        self.winner = -1
        self.current_agent = 0
        self.game = AcquireBoardState()
        self.hand = [[],[]] #The MOVES available for each agent. Will need to consistently update this after each step. 
        self.deck = []

    def copy_from_env(self, env):
        self.board = copy.deepcopy(env.unwrapped.board)
        self.agents = self.possible_agents[:]
        self.current_agent = env.unwrapped.agents.index(env.unwrapped.agent_selection)
        self.terminations = copy.deepcopy(env.unwrapped.terminations)
        self.winner = -1
        self.current_agent = copy.deepcopy(env.unwrapped.current_agent)
        self.game = copy.deepcopy(env.unwrapped.game)
        self.hand = copy.deepcopy(env.unwrapped.hand)
        self.deck = copy.deepcopy(env.unwrapped.deck)
        self.env = copy.deepcopy(env)
        for agent in env.unwrapped.rewards:
            if env.unwrapped.rewards[agent] > 0:
                self.winner = env.unwrapped.agents.index(agent)
        return
    
    def ACTIONS(self):
        return self.hand
    
    def RESULT(self,a):
        return self.env.step(a) #returns the new board state

    def reset(self):
        self.env.reset()

    def step(self,action):
        pass
    def check_for_winner(self):
        return self.env.check_for_winner()

    def print_board(self):
        return self.env.print_board()

'''
Need to figure out still: 
- need to add rewards as you play. Not just at the end?
-Make sure all methods are used, return what they need to, etc. 
-Test methods. Make sure they return and do what they are supposed to.

-Make a README file (and bullet points on powerpoint and more info in report.)
- Merge (if time)...
'''


#Action space is the tile grid position being placed. Can do calculations for this. 