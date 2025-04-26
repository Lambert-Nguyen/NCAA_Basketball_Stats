from fastapi import Depends
from src.app.service import Service
from src.app.req_res import PlayerSeasonsRequest, PlayerSeasonsResponse
from typing import Optional
# no need to import ConfigureBigQuery here

def include_route(base_router):
    # reuse the Service that was injected into the BaseRouter
    svc: Service = base_router.service

    @base_router.router.get(
        "/player/{player_name}/seasons",
        response_model=PlayerSeasonsResponse,
        summary="Per-season stats for one player"
    )
    def fetch_player_seasons(
        player_name: str,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None
    ):
        req = PlayerSeasonsRequest(
            player_name=player_name,
            start_year=start_year,
            end_year=end_year
        )
        return svc.get_player_seasons(req)