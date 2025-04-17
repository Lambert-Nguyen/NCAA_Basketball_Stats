from typing import Optional, List
from pydantic import BaseModel
from .models import PlayerName

""" Add req res models here """

class PlayerComparisonRequest(BaseModel):
    """
    Request model for comparing two players.

    This model is used to encapsulate the names of the two players 
    that will be compared using the PlayerComparisonQuery. It ensures 
    that the player names are provided in a structured and validated manner.

    Attributes:
        player1_name (PlayerName): The full name of the first player.
        player2_name (PlayerName): The full name of the second player.
    """
    player1_name: PlayerName
    player2_name: PlayerName



class PlayerComparisonResult(BaseModel):
    """
    Data model for player comparison results.

    This model is used to structure the data returned 
    after running a PlayerComparison BigQuery query. 
    It facilitates easy access and manipulation of the 
    comparison data in a structured format.
    """
    player1_name: Optional[str] = None
    player2_name: Optional[str] = None
    player1_position: Optional[str] = None
    player2_position: Optional[str] = None
    player1_team: Optional[str] = None
    player2_team: Optional[str] = None
    player1_goals: Optional[int] = None
    player2_goals: Optional[int] = None
    player1_assists: Optional[int] = None
    player2_assists: Optional[int] = None
    player1_efficiency: Optional[int] = None
    player2_efficiency: Optional[int] = None




class PlayerNameListRespone(BaseModel):
    """
    Model for storing a list of player names.

    This model is used to represent a list of player names 
    retrieved from a BigQuery result. It encapsulates a list 
    of PlayerName objects, providing a structured way to 
    manage multiple player names.

    Attributes:
        players (List[PlayerName]): A list of PlayerName objects, 
            each representing a player's full name.
    """
    players: List[PlayerName]



class StdResponse(BaseModel):
    message: str
    error: str | None = None
    data: dict | None = None
    status_code: int
    success: bool
    
    class Config:
        extra = "forbid"