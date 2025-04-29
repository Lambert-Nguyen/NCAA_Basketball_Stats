from src.app.router import BaseRouter
from src.utils.error_handler import ErrorHandler
from src.app.req_res import FetchTeamStatsEndpointReq

def include_route(routerobj: BaseRouter) -> None:
    @routerobj.router.post("/teams/stats")
    def fetch_team_stats(reqobj : FetchTeamStatsEndpointReq):
        try:
            result = routerobj.service.fetch_team_stats(reqobj.team_name, reqobj.season)
            return ErrorHandler.handle_success(
                data={"data": result},
                message="teams stats fetched successfully"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)