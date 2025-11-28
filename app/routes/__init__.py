from fastapi import APIRouter
from app.routes.summary import router as summary_router
router = APIRouter()
@router.get("/healthcheck")
async def healthcheck():
    return {
        "message": "Because he's the hero Gotham deserves, but not the one it needs right now. So we'll hunt him. Because he can take it. Because he's not our hero. He's a silent guardian, a watchful protector. A dark knight."}

router.include_router(summary_router)