FROM openjdk:slim
COPY --from=python:rc / /

WORKDIR /app

COPY ./main.py ./
COPY ./api.py ./
COPY ./init.py ./
COPY ./.env ./
COPY ./requirements.txt ./

RUN python3 -m pip install --upgrade -r requirements.txt && rm ./requirements.txt

RUN python3 ./init.py && rm ./init.py

CMD ["python", "./main.py"]
