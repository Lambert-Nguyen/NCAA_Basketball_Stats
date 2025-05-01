from src.app.router import BaseRouter
from src.utils.error_handler import ErrorHandler

def include_route(routerobj: BaseRouter) -> None:
    @routerobj.router.get("/teams")
    def fetch_all_teams():
        try:
            teams = routerobj.service.fetch_all_teams()
            return ErrorHandler.handle_success(
                data={"teams": teams},
                message="all teams fetched successfully"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)