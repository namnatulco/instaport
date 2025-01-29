# setup build env
FROM python:3-slim AS build-env
COPY . /app
WORKDIR /app

CMD ["pip install", "-r", "app/requirements.txt", "--root-user-action"]


# prod env
FROM gcr.io/distroless/python3
COPY --from=build-env /app /app
WORKDIR /app/app
CMD ["demo.py"]
