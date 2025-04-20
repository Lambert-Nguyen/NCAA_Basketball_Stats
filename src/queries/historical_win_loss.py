from src.app.req_res import HistoricalWinLossRequest
from src.queries.base_query import BaseQuery

class HistoricalWinLossQuery(BaseQuery):
    def __init__(self, request_obj : HistoricalWinLossRequest):
        super().__init__()
        self.team1code : int = request_obj.team1_code.ncaa_code
        self.team2code : int = request_obj.team2_code.ncaa_code
        self.build_query()

    """ this query takes 7.74 MB to execute as tested """
    def build_query(self) -> None:
        self.query = """
        SELECT 
            COALESCE(SUM(CASE WHEN win THEN 1 ELSE 0 END)) as wins, 
            COALESCE(SUM(CASE WHEN win THEN 0 ELSE 1 END)) as losses 
        FROM 
            `bigquery-public-data.ncaa_basketball.mbb_historical_teams_games` 
        WHERE 
            team_code = CAST(@team1_code AS string)
        AND 
            opp_code = @team2_code
        LIMIT 1000
        """



