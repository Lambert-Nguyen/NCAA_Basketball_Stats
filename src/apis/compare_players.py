from src.app.router import BaseRouter
from src.app.req_res import PlayerComparisonRequest
from src.utils.error_handler import ErrorHandler

def include_route(routerobj: BaseRouter) -> None:
    @routerobj.router.post("/players/compare")
    def compare_players(request: PlayerComparisonRequest):
        try:
            comparison = routerobj.service.compare_players(request=request)
            return ErrorHandler.handle_success(
                data={
                    "data" : comparison
                },
                message="player comparison successful"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)