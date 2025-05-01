from src.client.configure_bq import ConfigureBigQuery
from src.queries.fetch_names_query import FetchAllPlayerNamesQuery
from src.queries.player_compare import PlayerComparisonQuery, PlayerComparisonRequest
from src.queries.historical_win_loss import HistoricalWinLossQuery, HistoricalWinLossRequest
from src.queries.three_point_percent import ThreePointPercentRequest, ThreePointPercentQuery
from src.queries.team_performance import TeamPerformanceQuery, TeamPerformanceRequest
from src.queries.player_seasons import PlayerSeasonsQuery
from src.queries.player_games_query import PlayerGamesQuery
from src.queries.fetch_team_stats import FetchTeamStatsQuery
from src.queries.fetch_historical_matchups import FetchHistoricalMatchups
# from src.queries.fetch_all_teams import FetchAllTeamsQuery


from .req_res import PlayerSeasonsRequest
from .req_res import PlayerGamesRequest
from .req_res import FetchTeamStatsRequest
from .req_res import TeamComparisonRequest
from google.cloud import bigquery
from typing import Dict
from pandas import DataFrame



class Service:
    def __init__(self, client : ConfigureBigQuery, utils : Dict):
        self.client = client
        self.team_mapping = utils.get("team_mapping")
        self.predict_model = utils.get("prediction_model")
        self.project_id = utils.get("project_id")

    def fetch_player_names(self, result_size : int):
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
                     bigquery.ScalarQueryParameter("team2_code", "INT64", request.team2_code.ncaa_code),
                     bigquery.ScalarQueryParameter("starting_season", "INT64", request.starting_season),
                     bigquery.ScalarQueryParameter("ending_season", "INT64", request.ending_season)

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

    def get_team_performance(self, request: TeamPerformanceRequest):
        try:
            request.project_id = self.project_id
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

    def analyze_team_performance(self, request: TeamPerformanceRequest):
        try:
            request.project_id = self.project_id
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
            return {"teams": [dict(row) for row in result_list] if result_list else []}
        except Exception as e:
            raise e

    def get_top_offensive_teams(self, request: TeamPerformanceRequest):
        try:
            request.project_id = self.project_id
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

    def get_top_defensive_teams(self, request: TeamPerformanceRequest):
        try:
            request.project_id = self.project_id
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
            
    def get_player_seasons(self, req: PlayerSeasonsRequest):
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
    
    def get_player_games(self, request: PlayerGamesRequest):
        try : 
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
        
        except Exception as e :
            raise e 


    def predict_win_teams(self, team1_name: str, team2_name: str, season: int = 2017):
        try:
            # Get IDs from correct mapping
            team1_id = self.team_mapping.get(team1_name)  # Ensure nested access
            team2_id = self.team_mapping.get(team2_name)
            
            
            if not team1_id or not team2_id:
                raise ValueError("Team names not found")

            # Build queries
            team1_query = FetchTeamStatsQuery(FetchTeamStatsRequest(team_id=team1_id, season=season)).get_query()
            team2_query = FetchTeamStatsQuery(FetchTeamStatsRequest(team_id=team2_id, season=season)).get_query()

            
            # Job configs
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("team_id", "STRING", team1_id),
                    bigquery.ScalarQueryParameter("season", "INT64", season),
                ]
            )

            # Execute queries
            team1_stats = self.client.execute_query(
                query=team1_query,
                job_config=job_config
            ).to_dataframe().iloc[0].to_dict()

            job_config = bigquery.QueryJobConfig(  # Reuse config with new params
                query_parameters=[
                    bigquery.ScalarQueryParameter("team_id", "STRING", team2_id),
                    bigquery.ScalarQueryParameter("season", "INT64", season),
                ]
            )

            team2_stats = self.client.execute_query(
                query=team2_query,
                job_config=job_config
            ).to_dataframe().iloc[0].to_dict()

            # Prediction
            team1_stats['home_team'] = 1.0
            team2_stats['home_team'] = 0.0
            
            team1_prob = self.predict_model.predict_proba(DataFrame([team1_stats]))[0][1]
            team2_prob = self.predict_model.predict_proba(DataFrame([team2_stats]))[0][1]

            request = TeamComparisonRequest(team1_id=team1_id, team2_id=team2_id, season=season)

            fetch_historical_wins_query = FetchHistoricalMatchups(reqobj=request).get_query()

            job_config_historical_query = bigquery.QueryJobConfig(
                query_parameters=[
                bigquery.ScalarQueryParameter("team1_id", "STRING", team1_id),
                bigquery.ScalarQueryParameter("team2_id", "STRING", team2_id),
                bigquery.ScalarQueryParameter("season", "INT64", season),
                ]
            )

            return {
                'team1': team1_name,
                'team2': team2_name,
                'team1_win_prob': round(team1_prob, 3),
                'team2_win_prob': round(team2_prob, 3),
                'historical_matchups': [self.client.execute_query(query=fetch_historical_wins_query, job_config=job_config_historical_query).to_dataframe().to_dict('records')]
            }

        except Exception as e:
            raise ValueError(f"Prediction failed: {str(e)}")
    


    def fetch_all_teams(self):
        try:
            ''' Online version '''
            '''
            query = FetchAllTeamsQuery().get_query()
            result = [dict(row) for row in self.client.execute_query(query=query)]
            '''

            ''' Offline version'''
            result = self.team_mapping
            return result
            
        except Exception as e :
            raise e 
    
    def fetch_team_stats(self, team_name : str, season : int):
        try:
            team_id = self.team_mapping.get(team_name) 
            if not team_id:
                raise ValueError("Team name not found")

            # Build queries
            team_query = FetchTeamStatsQuery(FetchTeamStatsRequest(team_id=team_id, season=season)).get_query()
            
            # Job configs
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("team_id", "STRING", team_id),
                    bigquery.ScalarQueryParameter("season", "INT64", season),
                ]
            )

            team_stats = self.client.execute_query(
                query=team_query,
                job_config=job_config
            ).to_dataframe().iloc[0].to_dict()


            return team_stats
        
        except Exception as e :
            raise e 
    
    def fetch_historical_matchups(self, team1_name : str, team2_name : str, season : int):
        try:
             # Get IDs from correct mapping
            team1_id = self.team_mapping.get(team1_name)  # Ensure nested access
            team2_id = self.team_mapping.get(team2_name)
            
            
            if not team1_id or not team2_id:
                raise ValueError("Team names not found")


            # Build queries
            query = FetchHistoricalMatchups(TeamComparisonRequest(team1_id=team1_id, team2_id=team2_id, season=season)).get_query()
            
            # Job configs
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("team1_id", "STRING", team1_id),
                    bigquery.ScalarQueryParameter("team2_id", "STRING", team2_id),
                    bigquery.ScalarQueryParameter("season", "INT64", season),
                ]
            )

            res = self.client.execute_query(
                query=query,
                job_config=job_config
            ).to_dataframe().to_dict('records')


            return res
        
        except Exception as e :
            raise e 