from src.app.req_res import HistoricalWinLossRequest
from src.queries.base_query import BaseQuery

class HistoricalWinLossQuery(BaseQuery):
    def __init__(self, request_obj : HistoricalWinLossRequest):
        super().__init__()
        self.team1code : int = request_obj.team1_code.ncaa_code
        self.team2code : int = request_obj.team2_code.ncaa_code
        self.starting_season : int = request_obj.starting_season
        self.ending_season : int = request_obj.ending_season
        self.build_query()

    """ this query takes 35.96 MB to execute as tested """
    def build_query(self) -> None:
        self.query = """
        SELECT 
            market as team,
            COALESCE(SUM(CASE WHEN win THEN 1 ELSE 0 END)) as wins, 
            COALESCE(SUM(CASE WHEN win THEN 0 ELSE 1 END)) as losses,
            opp_market as opposing_team
        FROM 
            `bigquery-public-data.ncaa_basketball.mbb_historical_teams_games`
        WHERE 
            market="San Jose State University"
        AND 
            opp_market="San Diego State University"
        AND 
            season >= 2000
        AND
            season <= 2014

        GROUP BY team, opposing_team
        LIMIT 1000
        """



