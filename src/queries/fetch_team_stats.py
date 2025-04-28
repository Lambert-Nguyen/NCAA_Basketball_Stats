from src.queries.base_query import BaseQuery
from src.app.req_res import FetchTeamStatsRequest

class FetchTeamStatsQuery(BaseQuery):
    def __init__(self, reqobj : FetchTeamStatsRequest):
        super().__init__()
        self.team_id = reqobj.team_id
        self.season = reqobj.season
        self.build_query()
    
    """ this query takes 7.75 MB to execute as tested """
    def build_query(self) -> None:
        self.query = """
        SELECT 
            AVG(CASE WHEN home_team THEN 1.0 ELSE 0.0 END) as home_team, 
            AVG(points) as points,
            AVG(field_goals_pct) as field_goals_pct,
            AVG(three_points_pct) as three_points_pct,
            AVG(free_throws_pct) as free_throws_pct,
            AVG(rebounds) as rebounds,
            AVG(assists) as assists,
            AVG(turnovers) as turnovers,
            AVG(steals) as steals,
            AVG(blocks) as blocks,
            AVG(personal_fouls) as personal_fouls,
            AVG(fast_break_pts) as fast_break_pts,
            AVG(second_chance_pts) as second_chance_pts,
            AVG(points_off_turnovers) as points_off_turnovers
        FROM `bigquery-public-data.ncaa_basketball.mbb_teams_games_sr`
        WHERE team_id = @team_id AND season = @season
        """