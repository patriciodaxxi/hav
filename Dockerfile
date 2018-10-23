FROM node:10 as build-stage

WORKDIR /code/
COPY ./frontend/package.json frontend/yarn.lock ./
RUN yarn install
COPY ./frontend ./
RUN yarn build

FROM python:3.6-stretch
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y libpq-dev gcc ffmpeg libimage-exiftool-perl && \
    apt-get autoremove && \
    apt-get autoclean

RUN pip install -U pipenv

WORKDIR /hav/frontend
COPY --from=build-stage /code/build ./build

WORKDIR /hav/backend
COPY backend/Pipfile backend/Pipfile.lock ./

RUN pipenv install --system && pipenv install --system --dev

# Copy all backend files
COPY ./backend .

RUN ["python", "manage.py", "collectstatic", "--no-input"]

WORKDIR /hav

CMD ["uwsgi", "uwsgi.ini"]



