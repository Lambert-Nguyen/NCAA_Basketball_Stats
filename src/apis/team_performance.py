from src.app.router import BaseRouter
from src.app.req_res import TeamPerformanceRequest

from src.utils.error_handler import ErrorHandler

def include_route(routerobj: BaseRouter) -> None:
    @routerobj.router.get("/teams/performance")
    def get_team_performance(season: int = 2015):
        try:
            request = TeamPerformanceRequest(season=season)
            performance = routerobj.service.get_team_performance(request=request)
            return ErrorHandler.handle_success(
                data=performance,
                message="Team performance data retrieved successfully"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)

    @routerobj.router.get("/teams/performance/analyze")
    def analyze_team_performance(team_name: str, season: int = 2015):
        try:
            request = TeamPerformanceRequest(team_name=team_name, season=season)
            performance = routerobj.service.analyze_team_performance(request=request)
            return ErrorHandler.handle_success(
                data=performance,
                message=f"Performance data for {team_name} retrieved successfully"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)

    @routerobj.router.get("/teams/top/offensive")
    def get_top_offensive_teams(season: int = 2015, limit: int = 10):
        try:
            request = TeamPerformanceRequest(season=season, limit=limit)
            top_teams = routerobj.service.get_top_offensive_teams(request=request)
            return ErrorHandler.handle_success(
                data=top_teams,
                message="Top offensive teams retrieved successfully"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)

    @routerobj.router.get("/teams/top/defensive")
    def get_top_defensive_teams(season: int = 2015, limit: int = 10):
        try:
            request = TeamPerformanceRequest(season=season, limit=limit)
            top_teams = routerobj.service.get_top_defensive_teams(request=request)
            return ErrorHandler.handle_success(
                data=top_teams,
                message="Top defensive teams retrieved successfully"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)




    
        