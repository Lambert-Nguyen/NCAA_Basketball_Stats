from src.queries.base_query import BaseQuery


class FetchAllTeamsQuery(BaseQuery):
    def __init__(self,):
        super().__init__()
        self.build_query()
    
    """ this query takes 2.91 MB to execute as tested """
    def build_query(self) -> None:
        self.query = """
            SELECT 
                DISTINCT team_id, 
                market AS team_name
            FROM `bigquery-public-data.ncaa_basketball.mbb_teams_games_sr`
            WHERE market IS NOT NULL
            ORDER BY team_name
        """