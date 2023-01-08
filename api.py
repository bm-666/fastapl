import shutil
from uuid import uuid4

from starlette.responses import StreamingResponse
from starlette.templating import Jinja2Templates

from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks


from shemas import UploadVideo, GetVideo
from models import Video, User
from services import write_video, save_video

video_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@video_router.post("/")
async def create_video(
        back_tasks: BackgroundTasks,
        title: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...)
):
    user = await User.objects.first()
    return await save_video(user.dict().get("id"), file, title, description, back_tasks)

    




@video_router.post("/video")
async def create_video(video: Video):
    await video.save()
    return video

@video_router.get("/video/{v_pk}")
async def get_video(v_pk: int):
    file = await Video.objects.select_related("user").get(pk=v_pk)
    file_like = open(file.dict().get('file'), mode="rb")
    return  StreamingResponse(file_like, media_type="video/mp4")

