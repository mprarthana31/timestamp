ARG GIT_SHA

FROM python:3.11-alpine3.20 as builder

WORKDIR /code

COPY ./dev-requirements.txt ./

RUN pip install --no-cache-dir -r ./dev-requirements.txt

COPY . .

RUN pytest

FROM python:3.11-alpine3.20

ARG GIT_SHA

WORKDIR /code

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt

COPY --from=builder /code/app ./app

ENV GIT_SHA=${GIT_SHA}

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80"]