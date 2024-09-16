from rich import print
from fastapi import APIRouter, File, Form, UploadFile
from pydantic import ValidationError
from dtos.user_dto import UserDTO
from fastapi.exceptions import RequestValidationError
from services.user_service import UserService

router = APIRouter(
    prefix="/v1/users",
    tags=["Classes"],
    responses={404: {"description": "Not found methods for /classes"}},
)

user_service = UserService()


@router.get("")
def get_classes():
    print("Get all users")
    return user_service.listUsers()


@router.post("")
def add_classe(user: UserDTO):
    try:
        print(classe)
        created_classe = user_service.addUser(classe)
        print(f"{created_classe=}")
        return created_classe
    except ValidationError as e:
        print(e)
    except BaseException as er:
        print(er)
        return {"Error": er}
    

@router.get("/{id}")
def getById(id: str):
    return user_service.getUser(id)
