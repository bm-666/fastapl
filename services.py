import shutil

from uuid import  uuid4
from fastapi import UploadFile, Form, HTTPException, BackgroundTasks

from models import Video
from shemas import UploadVideo

async def save_video(
        user: int,
        file: UploadFile,
        title: str ,
        description: str,
        background_tasks: BackgroundTasks,
):
    file_name = f'media/{user}_{uuid4()}.mp4'
    if file.content_type == 'video/mp4':
        background_tasks.add_task(write_video, file_name, file)
    else:
        raise HTTPException(status_code=410, detail="It isn't mp4")
    info = UploadVideo(title=title, description=description)
    return await Video.objects.create(file=file_name, user=user, **info.dict())

def write_video(file_name: str, file: UploadFile):
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)