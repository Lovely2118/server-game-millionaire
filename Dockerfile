FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir  --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY app/main.py /code/main.py

CMD ["uvicorn", "app.main:fast_app", "--host", "0.0.0.0", "--port", "8000"]