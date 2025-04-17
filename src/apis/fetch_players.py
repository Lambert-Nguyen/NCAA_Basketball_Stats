from src.app.router import BaseRouter
from src.utils.error_handler import ErrorHandler

def include_route(routerobj: BaseRouter) -> None:
    @routerobj.router.get("/players/{size}")
    def fetch_players(size: int):
        try:
            players = routerobj.service.fetch_player_names(result_size=size)
            return ErrorHandler.handle_success(
                data={"players": players},
                message="players fetched successfully"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)