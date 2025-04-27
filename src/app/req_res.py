from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from .models import PlayerName, TeamCode, Player3PTFGStats

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
    
    

class HistoricalWinLossRequest(BaseModel):
    """
    Request model for comparing two team's win-loss
    
    Team Code from NCAA
    """
    team1_code: TeamCode
    team2_code: TeamCode



class HistoricalWinLossResults(BaseModel):
    """
    Data model for win-loss results.
    """
    
    wins: Optional[int] = None
    losses: Optional[int] = None
    
    
class ThreePointPercentRequest(BaseModel):
    """
    Request for getting three-point percentage leaders in a given season with at least min_shots attempts
    """
    season: int = 2015
    minimum_shots: int = 10
    

class ThreePointPercentResult(BaseModel):
    """
    Data model for player comparison results.

    This model is used to structure the data returned 
    after running a PlayerComparison BigQuery query. 
    It facilitates easy access and manipulation of the 
    comparison data in a structured format.
    """
    
    players: List[Player3PTFGStats] = None


class TeamPerformanceRequest(BaseModel):
    """Request model for team performance analysis.
    
    Attributes:
        season (Optional[int]): Single season year to analyze
        seasons (Optional[List[int]]): List of season years for comparison
        team_name (Optional[str]): Name of a single team to analyze
        team_names (Optional[List[str]]): List of team names for head-to-head
        limit (Optional[int]): Number of teams to return
        query_type (Optional[str]): Type of analysis ("all", "offensive", "defensive")
    """
    season: Optional[int] = None
    seasons: Optional[List[int]] = None
    team_name: Optional[str] = None
    team_names: Optional[List[str]] = None
    limit: Optional[int] = 10
    query_type: Optional[str] = "all"

class TeamPerformanceResponse(BaseModel):
    """Response model for team performance metrics.
    
    Attributes:
        team_name (str): Name of the team
        season (int): Season year
        win_percentage (float): Team's win percentage
        avg_points_scored (float): Average points scored per game
        avg_points_allowed (float): Average points allowed per game
        points_per_possession (float): Points scored per possession
        offensive_efficiency (float): Offensive efficiency rating
        defensive_efficiency (float): Defensive efficiency rating
    """
    team_name: Optional[str] = None
    season: Optional[int] = None
    win_percentage: Optional[float] = None
    avg_points_scored: Optional[float] = None
    avg_points_allowed: Optional[float] = None
    points_per_possession: Optional[float] = None
    offensive_efficiency: Optional[float] = None
    defensive_efficiency: Optional[float] = None

class TeamPerformanceListResponse(BaseModel):
    """Response model for list of team performances.
    
    Attributes:
        teams (List[TeamPerformanceResponse]): List of team performance metrics
    """
    teams: List[TeamPerformanceResponse]

class TopTeamsResponse(BaseModel):
    """Response model for top teams list.
    
    Attributes:
        teams (List[TeamPerformanceResponse]): List of top team performance metrics
    """
    teams: List[TeamPerformanceResponse] = []

    

class StdResponse(BaseModel):
    message: str
    error: Optional[str]
    data: Optional[dict]
    status_code: int
    success: bool
    
    class Config:
        extra = "forbid"
        
class PlayerSeasonsRequest(BaseModel):
    """
    GET /player/{player_name}/seasons
    """
    player_name: str
    start_year: Optional[int] = None
    end_year:   Optional[int] = None


class PlayerSeasonStats(BaseModel):
    player_name:   str
    season_year:   int
    games_played:  int
    total_points:  int
    avg_points:    float
    total_rebounds:  int
    avg_rebounds:    float
    total_assists:   int
    avg_assists:     float
    total_steals:    int
    avg_steals:      float
    total_blocks:    int
    avg_blocks:      float

class PlayerSeasonsResponse(BaseModel):
    seasons: List[PlayerSeasonStats]

class PlayerGamesRequest(BaseModel):
    player_name: str
    limit: Optional[int] = 20
    start_year: Optional[int] = None
    end_year: Optional[int] = None

class PlayerGame(BaseModel):
    player_name: str
    game_timestamp: Optional[datetime]
    minutes_played: Optional[int]
    points: Optional[int]
    rebounds: Optional[int]
    assists: Optional[int]
    steals: Optional[int]
    blocks: Optional[int]
    fgm: Optional[int]
    fga: Optional[int]
    fg_pct:  Optional[float]
    three_pt_made: Optional[int]
    three_pt_att: Optional[int]
    three_pt_pct: Optional[float]
    ftm: Optional[int]
    fta: Optional[int]
    ft_pct: Optional[float]

class PlayerGamesListResponse(BaseModel):
    games: List[PlayerGame]