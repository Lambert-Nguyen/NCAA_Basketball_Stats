from .req_res import PlayerNameListRespone
from src.client.configure_bq import ConfigureBigQuery
from src.queries.fetch_names_query import FetchAllPlayerNamesQuery
from src.queries.player_compare import PlayerComparisonQuery, PlayerComparisonRequest
from src.queries.historical_win_loss import HistoricalWinLossQuery, HistoricalWinLossRequest
from src.queries.three_point_percent import ThreePointPercentRequest, ThreePointPercentQuery
from src.queries.team_performance import TeamPerformanceQuery, TeamPerformanceRequest
from src.queries.player_seasons import PlayerSeasonsQuery
from src.queries.player_games_query import PlayerGamesQuery

from .models import PlayerName
from .req_res import PlayerComparisonResult
from .req_res import TeamPerformanceListResponse, TopTeamsResponse, TeamPerformanceResponse
from .req_res import PlayerSeasonsRequest, PlayerSeasonsResponse
from .req_res import PlayerGamesRequest, PlayerGamesListResponse
from google.cloud import bigquery


class Service:
    def __init__(self, client : ConfigureBigQuery):
        self.client = client

    def fetch_player_names(self, result_size : int) -> PlayerNameListRespone:
        try :
            query = FetchAllPlayerNamesQuery(result_size=result_size)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("result_size", "INT64", result_size),
                ]
            )
            result = self.client.execute_query(query.get_query(), job_config=job_config)

            return  [dict(row) for row in result]

        except Exception as e:
            raise e 
    
    def compare_players(self, request: PlayerComparisonRequest):
        try:
            query = PlayerComparisonQuery(request_obj=request)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("player1_name", "STRING", request.player1_name.full_name),
                     bigquery.ScalarQueryParameter("player2_name", "STRING", request.player2_name.full_name)
                ]
            )
            result = self.client.execute_query(query=query.get_query(), job_config=job_config)
    
            return [dict(row) for row in result] 
    
        except Exception as e :
            raise e 
    

    def historical_win_loss(self, request: HistoricalWinLossRequest):
        try:
            query = HistoricalWinLossQuery(request_obj=request)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("team1_code", "INT64", request.team1_code.ncaa_code),
                     bigquery.ScalarQueryParameter("team2_code", "INT64", request.team2_code.ncaa_code)
                ]
            )
            result = self.client.execute_query(query=query.get_query(), job_config=job_config)
    
            return [dict(row) for row in result] 
    
        except Exception as e :
            raise e 
        
    
    def three_point_percent(self, request: ThreePointPercentRequest):
        try:
            query = ThreePointPercentQuery(request_obj=request)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("season", "INT64", request.season),
                    bigquery.ScalarQueryParameter("minimum_shots", "INT64", request.minimum_shots),

                ]
            )
            result = self.client.execute_query(query=query.get_query(), job_config=job_config)
    
            return [dict(row) for row in result]
    
        except Exception as e :
            raise e 

    def get_team_performance(self, request: TeamPerformanceRequest) -> TeamPerformanceListResponse:
        try:
            query = TeamPerformanceQuery(request_obj=request)
            query_str = query.get_query()
            params = query.get_query_params()
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter(name, "INT64", value) if name == "season" else
                    bigquery.ArrayQueryParameter(name, "INT64", value) if name == "seasons" else
                    bigquery.ScalarQueryParameter(name, "STRING", value) if name == "team_name" else
                    bigquery.ArrayQueryParameter(name, "STRING", value)
                    for name, value in params.items()
                ]
            )
            result = self.client.execute_query(query=query_str, job_config=job_config)
            return {"teams": [dict(row) for row in result]}
        except Exception as e:
            raise e

    def analyze_team_performance(self, request: TeamPerformanceRequest) -> TeamPerformanceResponse:
        try:
            query = TeamPerformanceQuery(request_obj=request)
            query_str = query.get_query()
            params = query.get_query_params()
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter(name, "INT64", value) if name == "season" else
                    bigquery.ArrayQueryParameter(name, "INT64", value) if name == "seasons" else
                    bigquery.ScalarQueryParameter(name, "STRING", value)
                    for name, value in params.items()
                ]
            )
            result = self.client.execute_query(query=query_str, job_config=job_config)
            result_list = list(result)
            return {"team": dict(result_list[0]) if result_list else None}
        except Exception as e:
            raise e

    def get_top_offensive_teams(self, request: TeamPerformanceRequest) -> TopTeamsResponse:
        try:
            request.query_type = "offensive"
            query = TeamPerformanceQuery(request_obj=request)
            query_str = query.get_query()
            params = query.get_query_params()
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter(name, "INT64", value) if name == "season" else
                    bigquery.ArrayQueryParameter(name, "INT64", value) if name == "seasons" else
                    bigquery.ScalarQueryParameter(name, "INT64", value)
                    for name, value in params.items()
                ]
            )
            result = self.client.execute_query(query=query_str, job_config=job_config)
            return {"teams": [dict(row) for row in result]}
        except Exception as e:
            raise e

    def get_top_defensive_teams(self, request: TeamPerformanceRequest) -> TopTeamsResponse:
        try:
            request.query_type = "defensive"
            query = TeamPerformanceQuery(request_obj=request)
            query_str = query.get_query()
            params = query.get_query_params()
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter(name, "INT64", value) if name == "season" else
                    bigquery.ArrayQueryParameter(name, "INT64", value) if name == "seasons" else
                    bigquery.ScalarQueryParameter(name, "INT64", value)
                    for name, value in params.items()
                ]
            )
            result = self.client.execute_query(query=query_str, job_config=job_config)
            return {"teams": [dict(row) for row in result]}
        except Exception as e:
            raise e
            
    def get_player_seasons(self, req: PlayerSeasonsRequest) -> PlayerSeasonsResponse:
        try:
            q = PlayerSeasonsQuery(request_obj=req)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("player_name", "STRING", req.player_name),
                    bigquery.ScalarQueryParameter("start_year",  "INT64",  req.start_year),
                    bigquery.ScalarQueryParameter("end_year",    "INT64",  req.end_year),
                ]
            )
            rows = list(self.client.execute_query(q.get_query(), job_config=job_config))
            return {"seasons": [dict(r) for r in rows]}
        except Exception as e:
            raise e
    
    def get_player_games(self, request: PlayerGamesRequest) -> PlayerGamesListResponse:
        query = PlayerGamesQuery(request)
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("player_name", "STRING", request.player_name),
                bigquery.ScalarQueryParameter("limit",       "INT64",  request.limit),
                bigquery.ScalarQueryParameter("start_year",  "INT64",  request.start_year),
                bigquery.ScalarQueryParameter("end_year",    "INT64",  request.end_year),
            ]
        )
        result = self.client.execute_query(query.get_query(), job_config=job_config)
        return {"games": [dict(row) for row in result]}
