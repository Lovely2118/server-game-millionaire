import os.path
from pathlib import Path

from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse


def get_project_root():
    return Path(__file__).parent.parent.parent


def get_env_path():
    return os.path.join(get_project_root(), ".env")


def load_env():
    load_dotenv(get_env_path())


load_env()


def get_database_url():
    url_string = "postgresql://{}:{}@{}:{}/{}".format(
        os.environ.get("DATABASE-USER"),
        os.environ.get("DATABASE-PASSWORD"),
        os.environ.get("DATABASE-HOST"),
        os.environ.get("DATABASE-PORT"),
        os.environ.get("DATABASE-NAME")
    )
    return url_string


def check_entry_in_list(index: int, selected_list: list) -> bool:
    """
        Проверяем чтобы элемент входил в список
    :param index:
    :param selected_list:
    :return:
    """
    return 0 <= index < len(selected_list)


def get_json_response(answer: str) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"status": "error",
                                  "answer": answer}),
    )
