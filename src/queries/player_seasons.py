from .base_query import BaseQuery

class PlayerSeasonsQuery(BaseQuery):
    def __init__(self, request_obj):
        super().__init__()
        self.player_name = request_obj.player_name
        self.start_year  = request_obj.start_year
        self.end_year    = request_obj.end_year

    def get_query(self) -> str:
        return """
                WITH games AS (
                SELECT
                    full_name,
                    EXTRACT(YEAR FROM sp_created) AS season_year,
                    points,
                    rebounds,
                    assists,    
                    steals,
                    blocks
                FROM
                    `bigquery-public-data.ncaa_basketball.mbb_players_games_sr`
                WHERE
                    full_name = @player_name
                    AND (@start_year IS NULL OR EXTRACT(YEAR FROM sp_created) >= @start_year)
                    AND (@end_year   IS NULL OR EXTRACT(YEAR FROM sp_created) <= @end_year)
                )
                SELECT
                full_name                 AS player_name,
                season_year,
                COUNT(1)                  AS games_played,
                SUM(points)               AS total_points,
                ROUND(AVG(points), 2)     AS avg_points,
                SUM(rebounds)             AS total_rebounds,
                ROUND(AVG(rebounds), 2)   AS avg_rebounds,
                SUM(assists)              AS total_assists,
                ROUND(AVG(assists), 2)    AS avg_assists,
                SUM(steals)               AS total_steals,
                ROUND(AVG(steals), 2)     AS avg_steals,
                SUM(blocks)               AS total_blocks,
                ROUND(AVG(blocks), 2)     AS avg_blocks
                FROM
                games
                GROUP BY
                full_name,
                season_year
                ORDER BY
                season_year
                """