from src.app.router import BaseRouter
from src.app.req_res import HistoricalWinLossRequest
from src.utils.error_handler import ErrorHandler

def include_route(routerobj: BaseRouter) -> None:
    @routerobj.router.post("/teams/win-loss")
    def historical_win_loss(request: HistoricalWinLossRequest):
        try:
            win_loss = routerobj.service.historical_win_loss(request=request)
            return ErrorHandler.handle_success(
                data={
                    "data" : win_loss
                },
                message="win-loss request successful"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)