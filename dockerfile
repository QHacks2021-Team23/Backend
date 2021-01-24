FROM python:3-slim

WORKDIR /app

COPY ./main.py ./
COPY ./api.py ./

COPY ./requirements.txt ./
RUN python3 -m pip install --upgrade -r requirements.txt && rm ./requirements.txt

CMD ["python", "./main.py"]


