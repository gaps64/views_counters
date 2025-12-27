from typing import TYPE_CHECKING
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from counters_api.container import Container

if TYPE_CHECKING:
    from service.views_service import ViewsService

router = APIRouter(
    prefix='/videos'
)


@router.post("/{video_id}/view")
@inject
async def add_view(
    video_id: int, 
    service: "ViewsService" = Depends(Provide(Container.views_service))
) -> None:
    return await service.add_view(video_id)



@router.get("/{video_id}/views")
@inject
async def get_views(
    video_id: int, 
    service: "ViewsService" = Depends(Provide(Container.views_service))
) -> None:
    return await service.get_views(video_id)


