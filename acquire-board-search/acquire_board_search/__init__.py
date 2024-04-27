from gymnasium.envs.registration import register

from acquire_board_search.envs.acquire_board_search_env import raw_env
from acquire_board_search.envs.acquire_board_search_model import AcquireBoardModel
from acquire_board_search.envs.acquire_board_search_model import AcquireBoardState

register(
    id="acquire_board_search/AquireBoardSearch-v0",

    entry_point="acquire_board_search.envs:raw_env",

    max_episode_steps=100,
)