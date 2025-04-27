from fastapi import Depends
from typing import Optional
from src.app.service import Service
from src.app.req_res import PlayerGamesRequest, PlayerGamesListResponse

def include_route(base_router):
    svc: Service = base_router.service

    @base_router.router.get(
        "/player/{player_name}/games",
        response_model=PlayerGamesListResponse,
        summary="Play-by-play or per-game detail for one player"
    )
    def fetch_player_games(
        player_name: str,
        limit: Optional[int]     = 20,
        start_year: Optional[int] = None,
        end_year: Optional[int]   = None
    ):
        req = PlayerGamesRequest(
            player_name=player_name,
            limit=limit,
            start_year=start_year,
            end_year=end_year
        )
        return svc.get_player_games(req)
