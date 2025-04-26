from src.app.req_res import TeamPerformanceRequest
from src.queries.base_query import BaseQuery
from typing import List, Optional

class TeamPerformanceQuery(BaseQuery):
    def __init__(self, request_obj: TeamPerformanceRequest):
        super().__init__()
        self.season: Optional[int] = request_obj.season
        self.seasons: Optional[List[int]] = request_obj.seasons
        self.team_name: Optional[str] = request_obj.team_name
        self.team_names: Optional[List[str]] = request_obj.team_names
        self.limit: Optional[int] = request_obj.limit
        self.query_type: str = request_obj.query_type or "all"
        self.validate_inputs()
        self.build_query()

    def validate_inputs(self) -> None:
        """Validate request parameters to prevent invalid queries."""
        if self.season and self.seasons:
            raise ValueError("Cannot specify both season and seasons")
        if not (self.season or self.seasons):
            self.seasons = [2013, 2014, 2015]  # Default seasons
        if self.limit and (self.limit < 1 or self.limit > 100):
            raise ValueError("Limit must be between 1 and 100")
        if self.query_type not in ["all", "offensive", "defensive"]:
            raise ValueError("Query type must be 'all', 'offensive', or 'defensive'")
        if self.team_name and self.team_names:
            raise ValueError("Cannot specify both team_name and team_names")

    def build_query(self) -> None:
        """Build parameterized query for team performance metrics."""
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
            -- Possession formula using offensive rebounds
            SUM(h_field_goals_att - h_offensive_rebounds + h_turnovers + 0.475 * h_free_throws_att) AS total_possessions
          FROM
            `bigquery-public-data.ncaa_basketball.mbb_games_sr`
          WHERE
            {season_filter}
            AND h_points_game IS NOT NULL
            AND a_points_game IS NOT NULL
            AND h_market IS NOT NULL
            {team_filter_home}
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
            SUM(a_field_goals_att - a_offensive_rebounds + a_turnovers + 0.475 * a_free_throws_att) AS total_possessions
          FROM
            `bigquery-public-data.ncaa_basketball.mbb_games_sr`
          WHERE
            {season_filter}
            AND a_points_game IS NOT NULL
            AND h_points_game IS NOT NULL
            AND a_market IS NOT NULL
            {team_filter_away}
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
            (wins / NULLIF(games_played, 0)) AS win_percentage,
            (total_points_scored / NULLIF(games_played, 0)) AS avg_points_scored,
            (total_points_allowed / NULLIF(games_played, 0)) AS avg_points_allowed,
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
        {order_by}
        {limit_clause}
        """

        # Set season filter
        season_filter = "season = @season" if self.season else "season IN UNNEST(@seasons)"

        # Set team filter for head-to-head analysis
        team_filter_home = ""
        team_filter_away = ""
        if self.team_name:
            team_filter_home = "AND h_market = @team_name"
            team_filter_away = "AND a_market = @team_name"
        elif self.team_names:
            team_filter_home = "AND h_market IN UNNEST(@team_names)"
            team_filter_away = "AND a_market IN UNNEST(@team_names)"

        # Set order by clause
        order_by = ""
        if self.query_type == "offensive":
            order_by = "ORDER BY offensive_efficiency DESC"
        elif self.query_type == "defensive":
            order_by = "ORDER BY defensive_efficiency ASC"
        else:
            order_by = "ORDER BY season, team_name, offensive_efficiency DESC"

        # Set limit clause
        limit_clause = f"LIMIT {self.limit}" if self.limit else ""

        # Format query
        self.query = base_query.format(
            season_filter=season_filter,
            team_filter_home=team_filter_home,
            team_filter_away=team_filter_away,
            order_by=order_by,
            limit_clause=limit_clause
        )

    def set_query_type(self, query_type: str) -> None:
        """Set the type of query (all, offensive, defensive)."""
        self.query_type = query_type
        self.validate_inputs()
        self.build_query()

    def get_query_params(self) -> dict:
        """Return query parameters for BigQuery based on query requirements."""
        params = {}
        if self.season:
            params["season"] = self.season
        elif self.seasons:
            params["seasons"] = self.seasons
        if self.team_name:
            params["team_name"] = self.team_name
        elif self.team_names:
            params["team_names"] = self.team_names
        return params