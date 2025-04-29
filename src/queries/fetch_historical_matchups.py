from src.queries.base_query import BaseQuery
from src.app.req_res import TeamComparisonRequest


class FetchHistoricalMatchups(BaseQuery):
    def __init__(self, reqobj : TeamComparisonRequest):
        super().__init__()
        self.team1_id = reqobj.team1_id
        self.team2_id = reqobj.team2_id
        self.season = reqobj.season
        self.build_query()
        
    """ this query takes 6.66 MB to execute as tested """
    def build_query(self) -> None:
        self.query = """
    WITH matchups AS (
      SELECT
        g.game_id,
        g.scheduled_date,
        t1.market AS team1,
        t2.market AS team2,
        CASE WHEN t1.win THEN t1.market ELSE t2.market END AS winner
      FROM `bigquery-public-data.ncaa_basketball.mbb_games_sr` g
      JOIN `bigquery-public-data.ncaa_basketball.mbb_teams_games_sr` t1
        ON g.game_id = t1.game_id
      JOIN `bigquery-public-data.ncaa_basketball.mbb_teams_games_sr` t2
        ON g.game_id = t2.game_id AND t1.team_id < t2.team_id
      WHERE ((t1.team_id = @team1_id AND t2.team_id = @team2_id)
          OR (t1.team_id = @team2_id AND t2.team_id = @team1_id))
        AND g.season <= @season
    )
    SELECT * FROM matchups
    """
        