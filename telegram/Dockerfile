FROM python:3.10

WORKDIR /bot

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /bot/
CMD ["python3", "./telegram/main.py"]