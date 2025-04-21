from src.app.req_res import TeamPerformanceRequest
from src.queries.base_query import BaseQuery

class TeamPerformanceQuery(BaseQuery):
    def __init__(self, request_obj : TeamPerformanceRequest):
        super().__init__()
        self.season : int = request_obj.season
        self.team_name : str = request_obj.team_name
        self.limit : int = request_obj.limit
        self.query_type : str = request_obj.query_type
        self.build_query()

    def build_query(self) -> None:
        """ this query takes 3 MB to execute as tested """
        base_query = """
        WITH GameStats AS (
          -- Aggregate stats for home teams
          SELECT
            h_market AS team_name,
            season,
            COUNT(*) AS games_played,
            SUM(CASE WHEN h_points_game > a_points_game THEN 1 ELSE 0 END) AS wins,
            SUM(h_points_game) AS total_points_scored,
            SUM(a_points_game) AS total_points_allowed,
            SUM(h_field_goals_att - h_rebounds + h_turnovers + 0.475 * h_free_throws_att) AS total_possessions
          FROM
            `bigquery-public-data.ncaa_basketball.mbb_games_sr`
          WHERE
            season = @season
            AND h_points_game IS NOT NULL
            AND a_points_game IS NOT NULL
          GROUP BY
            h_market, season

          UNION ALL

          -- Aggregate stats for away teams
          SELECT
            a_market AS team_name,
            season,
            COUNT(*) AS games_played,
            SUM(CASE WHEN a_points_game > h_points_game THEN 1 ELSE 0 END) AS wins,
            SUM(a_points_game) AS total_points_scored,
            SUM(h_points_game) AS total_points_allowed,
            SUM(a_field_goals_att - a_rebounds + a_turnovers + 0.475 * a_free_throws_att) AS total_possessions
          FROM
            `bigquery-public-data.ncaa_basketball.mbb_games_sr`
          WHERE
            season = @season
            AND a_points_game IS NOT NULL
            AND h_points_game IS NOT NULL
          GROUP BY
            a_market, season
        ),
        TeamAggregates AS (
            -- Combine home and away stats for each team
            SELECT
              team_name,
              season,
              SUM(games_played) AS games_played,
              SUM(wins) AS wins,
              SUM(total_points_scored) AS total_points_scored,
              SUM(total_points_allowed) AS total_points_allowed,
              SUM(total_possessions) AS total_possessions
            FROM
              GameStats
            GROUP BY
              team_name, season
        ),
        TeamMetrics AS (
          -- Calculate performance metrics
          SELECT
            team_name,
            season,
            games_played,
            wins,
            (wins / games_played) AS win_percentage,
            (total_points_scored / games_played) AS avg_points_scored,
            (total_points_allowed / games_played) AS avg_points_allowed,
            (total_points_scored / NULLIF(total_possessions, 0)) AS points_per_possession,
            (100 * total_points_scored / NULLIF(total_possessions, 0)) AS offensive_efficiency,
            (100 * total_points_allowed / NULLIF(total_possessions, 0)) AS defensive_efficiency
          FROM
            TeamAggregates
          WHERE
            total_possessions > 0
        )
        SELECT
          team_name,
          season,
          ROUND(win_percentage, 3) AS win_percentage,
          ROUND(avg_points_scored, 1) AS avg_points_scored,
          ROUND(avg_points_allowed, 1) AS avg_points_allowed,
          ROUND(points_per_possession, 3) AS points_per_possession,
          ROUND(offensive_efficiency, 1) AS offensive_efficiency,
          ROUND(defensive_efficiency, 1) AS defensive_efficiency
        FROM
          TeamMetrics
        WHERE
          games_played >= 10
        """

        # Add specific filters based on query type
        if self.team_name:
            base_query += " AND team_name = @team_name"
        elif self.query_type == "offensive":
            base_query += " ORDER BY offensive_efficiency DESC"
            if self.limit:
                base_query += f" LIMIT {self.limit}"
        elif self.query_type == "defensive":
            base_query += " ORDER BY defensive_efficiency ASC"
            if self.limit:
                base_query += f" LIMIT {self.limit}"
        else:
            base_query += " ORDER BY offensive_efficiency DESC"

        self.query = base_query

    def set_query_type(self, query_type: str) -> None:
        """Set the type of query (all, offensive, defensive)"""
        self.query_type = query_type
        self.build_query()
        
