
import json
import pathlib
from typing import List

from fastapi import (APIRouter, File, Query, UploadFile,
                     status)
from fastapi.param_functions import Depends
from fastapi.responses import FileResponse, JSONResponse

from app.queries import photo
from app.auth.oauth2 import get_current_user
from app.exceptions import ForbiddenException, ProductFileNotFoundException
from app.queries.customer import get_user_role
from app.routers.delete import deletfilesproduct
from app.routers.download import downloadfilesproduct

photo_router = APIRouter(tags=["Photo"])


@photo_router.get('/product/{product_id}/photo/{image_name}')
async def get_product_photo_by_name(product_id: int = Query(None, description='Id продукта'),
                                    image_name: str = Query(None, description='Имя файла')) -> FileResponse:

    folder_path = pathlib.Path(__file__).parent.resolve()
    # проверка на существование файла
    file_path = folder_path.joinpath(pathlib.Path(f"assets/{image_name}"))
    # TODO: Добавить в Exception
    if not pathlib.Path.is_file(file_path):
        raise ProductFileNotFoundException
    return FileResponse(file_path)


@photo_router.get('/product/{product_id}/photos')
async def get_product_photo_all_filename(product_id: int = Query(None, description='Id продукта')) -> list:

    return await photo.get_all_name_photo(product_id)


@photo_router.delete('/product/{product_id}/photo')
async def delete_product_photo(product_id: int = Query(None, description='Id продукта'),
                               key: str = Query(None, description='photoid'),
                               current_user: str = Depends(get_current_user)) -> JSONResponse:
    role = await get_user_role(current_user)
    if not role:
        raise ForbiddenException
    image_name = await photo.delete_photo_by_name(product_id, key)

    image_name = json.loads(image_name.replace("'", '"'))
    if not image_name:
        raise ProductFileNotFoundException
    await deletfilesproduct(image_name)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'details': 'Файл удален',
    })


@photo_router.post('/product/{product_id}/photo')
async def add_photo(upload_files: List[UploadFile] = File(...),
                    current_user: str = Depends(get_current_user)) -> JSONResponse:
    role = await get_user_role(current_user)
    if not role:
        raise ForbiddenException
    await downloadfilesproduct(upload_files)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed',
    })
