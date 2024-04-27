from acquire_board_search import AcquireBoardState
from acquire_board_search import raw_env
import random

game = AcquireBoardState()

def test_generate_tile_name():
    position_x = int(input("Input a x position"))
    position_y = int(input("input a y position"))
    position = (position_x,position_y)
    name = game.generate_tile_name(position)
    print(name)
    return name


def test_generate_tile():
    tile = game.generate_tile()
    print("Grid Position",tile.GET_POSITION())
    print("In-Game Position", tile.GET_GAME_POSITION())
    return tile


def test_draw_function():
    drawn_tile = game.draw()
    updated_list = game.tiles_drawn
    print("updated list", updated_list)
    print("Grid position",drawn_tile.GET_POSITION())
    print("In-Game Position", drawn_tile.GET_GAME_POSITION())
    return drawn_tile

def test_printing_board():
    env = raw_env("ascii")
    env.reset()
    for i in range(10):
        observation, reward, termination, truncation, info = env.last()
        hands = observation["hands"]
        hands = hands.tolist()
        print("player hands",hands)
        env.print_board()
        cur_agent = observation["current"]
        cur_agent = cur_agent
        print("current agent",cur_agent)
        choice = random.sample(hands[cur_agent],1)
        print("choice made",choice)
        action = choice[0]
        env.step(action)
    env.print_board()
    return

#test_generate_tile_name()
#test_generate_tile()
#test_draw_function()
#test_draw_function()
test_printing_board()
