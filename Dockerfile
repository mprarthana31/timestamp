FROM python:3.11-alpine3.20 as builder

ARG GIT_SHA

ARG BUILD_DATE

WORKDIR /code

COPY ./dev-requirements.txt ./

RUN pip install --no-cache-dir -r ./dev-requirements.txt

COPY . .

RUN pytest

FROM python:3.11-alpine3.20

ARG GIT_SHA

ARG BUILD_DATE

WORKDIR /code

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt

COPY --from=builder /code/app ./app

ENV GIT_SHA=${GIT_SHA}

ENV BUILD_DATE=${BUILD_DATE}

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80"]