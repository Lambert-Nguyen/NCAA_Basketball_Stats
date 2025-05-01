from src.app.router import BaseRouter
from src.app.req_res import WinPredictionRequest
from src.utils.error_handler import ErrorHandler

def include_route(routerobj: BaseRouter) -> None:
    @routerobj.router.post("/teams/predict-winner")
    def predict_winner(request: WinPredictionRequest):
        try:
            prediction_result = routerobj.service.predict_win_teams(team1_name=request.team1_name, team2_name=request.team2_name)
            return ErrorHandler.handle_success(
                data={
                    "result" : prediction_result
                },
                message="prediction result generation successful"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)