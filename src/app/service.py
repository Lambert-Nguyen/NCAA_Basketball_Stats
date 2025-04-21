from .req_res import PlayerNameListRespone
from src.client.configure_bq import ConfigureBigQuery
from src.queries.fetch_names_query import FetchAllPlayerNamesQuery
from src.queries.player_compare import PlayerComparisonQuery, PlayerComparisonRequest
from src.queries.historical_win_loss import HistoricalWinLossQuery, HistoricalWinLossRequest
from src.queries.team_performance import TeamPerformanceQuery, TeamPerformanceRequest
from .models import PlayerName
from .req_res import PlayerComparisonResult
from .req_res import TeamPerformanceListResponse, TopTeamsResponse, TeamPerformanceResponse

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

    def get_team_performance(self, request: TeamPerformanceRequest) -> TeamPerformanceListResponse:
        try:
            query = TeamPerformanceQuery(request_obj=request)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("season", "INT64", request.season)
                ]
            )
            result = self.client.execute_query(query=query.get_query(), job_config=job_config)
            return {"teams": [dict(row) for row in result]}
        except Exception as e:
            raise e

    def analyze_team_performance(self, request: TeamPerformanceRequest) -> TeamPerformanceResponse:
        try:
            query = TeamPerformanceQuery(request_obj=request)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("season", "INT64", request.season),
                    bigquery.ScalarQueryParameter("team_name", "STRING", request.team_name)
                ]
            )
            result = self.client.execute_query(query=query.get_query(), job_config=job_config)
            result_list = list(result)
            return {"team": dict(result_list[0]) if result_list else None}
        except Exception as e:
            raise e

    def get_top_offensive_teams(self, request: TeamPerformanceRequest) -> TopTeamsResponse:
        try:
            request.query_type = "offensive"
            query = TeamPerformanceQuery(request_obj=request)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("season", "INT64", request.season),
                    bigquery.ScalarQueryParameter("limit", "INT64", request.limit)
                ]
            )
            result = self.client.execute_query(query=query.get_query(), job_config=job_config)
            result_list = list(result)
            return {"team": dict(result_list[0]) if result_list else None}
        except Exception as e:
            raise e

    def get_top_defensive_teams(self, request: TeamPerformanceRequest) -> TopTeamsResponse:
        try:
            request.query_type = "defensive"
            query = TeamPerformanceQuery(request_obj=request)
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("season", "INT64", request.season),
                    bigquery.ScalarQueryParameter("limit", "INT64", request.limit)
                ]
            )
            result = self.client.execute_query(query=query.get_query(), job_config=job_config)
            result_list = list(result)
            return {"team": dict(result_list[0]) if result_list else None}
        except Exception as e:
            raise e 
        
    