from src.app.req_res import PlayerComparisonRequest
from src.queries.base_query import BaseQuery

class PlayerComparisonQuery(BaseQuery):
    def __init__(self, request_obj : PlayerComparisonRequest):
        super().__init__()
        self.player1 : str = request_obj.player1_name.full_name
        self.player2 : str = request_obj.player2_name.full_name
        self.build_query()

    """ this query takes 58.39 MB to execute as tested """
    def build_query(self) -> None:
        self.query = """
        WITH PlayerData AS (
        SELECT
            full_name,
            team_name,
            primary_position,
            SUM(field_goals_made) AS total_goals,
            SUM(assists) AS total_assists,
            SUM(offensive_rebounds) as total_orebs,
            SUM(defensive_rebounds) as total_drebs,
            SUM(steals) as total_steals,
            SUM(blocks) as total_blocks,
            SUM(turnovers) as total_turnovers
        FROM
            `bigquery-public-data.ncaa_basketball.mbb_players_games_sr`
        WHERE
            full_name IN (@player1_name, @player2_name)
        GROUP BY full_name, team_name, primary_position
        ),
        Player1 AS (
        SELECT * FROM PlayerData WHERE full_name = @player1_name
        ),
        Player2 AS (
        SELECT * FROM PlayerData WHERE full_name = @player2_name
        )
        SELECT
        P1.full_name AS player1_name,
        P2.full_name AS player2_name,
        P1.primary_position as player1_position,
        P2.primary_position as player2_position,
        P1.team_name AS player1_team,
        P2.team_name AS player2_team,
        P1.total_goals AS player1_goals,
        P2.total_goals AS player2_goals,
        P1.total_assists AS player1_assists,
        P2.total_assists AS player2_assists,
        (P1.total_goals + P1.total_assists + P1.total_orebs + P1.total_drebs + P1.total_steals + P1.total_blocks - P1.total_turnovers) AS player1_efficiency,
        (P2.total_goals + P2.total_assists + P2.total_orebs + P2.total_drebs + P2.total_steals + P2.total_blocks - P2.total_turnovers) AS player2_efficiency
        FROM
        Player1 P1,
        Player2 P2
        """
        
       
    def escape_name(self, name : str) -> str:
        """Escapes single quotes in player names for BigQuery."""
        return name.replace("'", "\\'")



