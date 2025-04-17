from src.queries.base_query import BaseQuery

class FetchAllPlayerNamesQuery(BaseQuery):
    def __init__(self, result_size : int):
        super().__init__()
        self.result_size = result_size
        self.build_query()
    
    """ this query takes 12.73 MB to execute as tested """
    def build_query(self) -> None:
        self.query = """
        SELECT 
        DISTINCT full_name AS full_name
        FROM 
        `bigquery-public-data.ncaa_basketball.mbb_players_games_sr`
        ORDER BY 
        full_name
        LIMIT @result_size 
        """

     