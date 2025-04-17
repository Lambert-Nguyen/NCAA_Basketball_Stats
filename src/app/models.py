
from typing import List 
from pydantic import BaseModel

class PlayerName(BaseModel):
    """
    Model for storing a player's full name.

    This model is used to represent a player's full name 
    as retrieved from a BigQuery result. It is designed to 
    handle a single player name and is particularly useful 
    when fetching a list of player names.

    Attributes:
        full_name (str): The full name of the player.
    """
    full_name: str


