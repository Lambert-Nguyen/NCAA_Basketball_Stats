from src.app.router import BaseRouter
from src.utils.error_handler import ErrorHandler
from src.app.req_res import FetchHistoricalMatchupEndpointReq

def include_route(routerobj: BaseRouter) -> None:
    @routerobj.router.post("/teams/past-matchups")
    def fetch_historical_matchups(reqobj : FetchHistoricalMatchupEndpointReq):
        try:
            result = routerobj.service.fetch_historical_matchups(reqobj.team1_name, reqobj.team2_name, reqobj.season)
            return ErrorHandler.handle_success(
                data={"data": result},
                message="team matchups data fetched successfully"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)