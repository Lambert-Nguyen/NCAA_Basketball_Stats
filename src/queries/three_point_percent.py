from src.app.req_res import ThreePointPercentRequest, ThreePointPercentResult
from src.queries.base_query import BaseQuery

class ThreePointPercentQuery(BaseQuery):
    def __init__(self, request_obj : ThreePointPercentRequest):
        super().__init__()
        self.season: int = request_obj.season
        self.minimum_shots: int = request_obj.minimum_shots
        self.build_query()

    """ this query takes 61.36 MB to execute as tested """
    def build_query(self) -> None:
        self.query = """
        SELECT 
            full_name, 
            player_id, 
            SUM(three_points_made) * 1.0 / SUM(three_points_att) as three_point_pct
        FROM 
            `bigquery-public-data.ncaa_basketball.mbb_players_games_sr`
        WHERE 
            season = @season 
        GROUP BY 
            player_id, full_name 
        HAVING 
            SUM(three_points_att) > @minimum_shots
        ORDER BY three_point_pct DESC 
        LIMIT 10
        """



