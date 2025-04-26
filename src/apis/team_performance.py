from src.app.router import BaseRouter
from src.app.req_res import TeamPerformanceRequest
from src.utils.error_handler import ErrorHandler
from typing import List, Optional
from fastapi import Query

def include_route(routerobj: BaseRouter) -> None:
    @routerobj.router.get("/teams/performance")
    async def get_team_performance(
        season: Optional[int] = None,
        seasons: Optional[List[int]] = Query(None)
    ):
        try:
            request = TeamPerformanceRequest(season=season, seasons=seasons)
            performance = routerobj.service.get_team_performance(request=request)
            return ErrorHandler.handle_success(
                data=performance,
                message="Team performance data retrieved successfully"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)

    @routerobj.router.get("/teams/performance/analyze")
    async def analyze_team_performance(
        team_name: str,
        season: Optional[int] = None,
        seasons: Optional[List[int]] = Query(None)
    ):
        try:
            request = TeamPerformanceRequest(team_name=team_name, season=season, seasons=seasons)
            performance = routerobj.service.analyze_team_performance(request=request)
            return ErrorHandler.handle_success(
                data=performance,
                message=f"Performance data for {team_name} retrieved successfully"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)

    @routerobj.router.get("/teams/performance/head-to-head")
    async def head_to_head_performance(
        team_names: List[str] = Query(...),
        season: Optional[int] = None,
        seasons: Optional[List[int]] = Query(None)
    ):
        try:
            request = TeamPerformanceRequest(team_names=team_names, season=season, seasons=seasons)
            performance = routerobj.service.get_team_performance(request=request)
            return ErrorHandler.handle_success(
                data=performance,
                message=f"Head-to-head performance data for {', '.join(team_names)} retrieved successfully"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)

    @routerobj.router.get("/teams/top/offensive")
    async def get_top_offensive_teams(
        season: Optional[int] = None,
        seasons: Optional[List[int]] = Query(None),
        limit: int = 10
    ):
        try:
            request = TeamPerformanceRequest(season=season, seasons=seasons, limit=limit, query_type="offensive")
            top_teams = routerobj.service.get_top_offensive_teams(request=request)
            return ErrorHandler.handle_success(
                data=top_teams,
                message="Top offensive teams retrieved successfully"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)

    @routerobj.router.get("/teams/top/defensive")
    async def get_top_defensive_teams(
        season: Optional[int] = None,
        seasons: Optional[List[int]] = Query(None),
        limit: int = 10
    ):
        try:
            request = TeamPerformanceRequest(season=season, seasons=seasons, limit=limit, query_type="defensive")
            top_teams = routerobj.service.get_top_defensive_teams(request=request)
            return ErrorHandler.handle_success(
                data=top_teams,
                message="Top defensive teams retrieved successfully"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)