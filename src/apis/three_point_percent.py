from src.app.router import BaseRouter
from src.app.req_res import ThreePointPercentRequest
from src.utils.error_handler import ErrorHandler

def include_route(routerobj: BaseRouter) -> None:
    @routerobj.router.post("/players/three-point-percent")
    def three_point_percent(request: ThreePointPercentRequest):
        try:
            players = routerobj.service.three_point_percent(request=request)
            return ErrorHandler.handle_success(
                data={
                    "data" : players
                },
                message="3pt percent request successful"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)