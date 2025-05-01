from .base_query import BaseQuery

class PlayerGamesQuery(BaseQuery):
    def __init__(self, request_obj):
        # super().__init__(request_obj)
        self.player_name = request_obj.player_name
        self.limit       = request_obj.limit
        self.start_year  = request_obj.start_year
        self.end_year    = request_obj.end_year

    def get_query(self) -> str:
        return """
        SELECT
          full_name                            AS player_name,
          sp_created                           AS game_timestamp,
          CAST(minutes_int64 AS INT64)         AS minutes_played,
          points,
          rebounds,
          assists,
          steals,
          blocks,
          field_goals_made                     AS fgm,
          field_goals_att                      AS fga,
          ROUND(field_goals_pct, 3)            AS fg_pct,
          three_points_made                    AS three_pt_made,
          three_points_att                     AS three_pt_att,
          ROUND(three_points_pct, 3)           AS three_pt_pct,
          free_throws_made                     AS ftm,
          free_throws_att                      AS fta,
          ROUND(free_throws_pct, 3)            AS ft_pct
        FROM
          `bigquery-public-data.ncaa_basketball.mbb_players_games_sr`
        WHERE
          full_name = @player_name
          AND (@start_year IS NULL OR EXTRACT(YEAR FROM sp_created) >= @start_year)
          AND (@end_year   IS NULL OR EXTRACT(YEAR FROM sp_created) <= @end_year)
        ORDER BY
          sp_created DESC
        LIMIT @limit
        """
