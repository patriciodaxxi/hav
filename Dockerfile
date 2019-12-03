FROM node:12 as build-stage

WORKDIR /code/

# Link up the required build files
COPY ./frontend/package.json ./frontend/yarn.lock ./frontend/babel.config.json ./
COPY ./frontend/admin/package.json ./admin/
COPY ./frontend/ui/package.json ./ui/
COPY ./frontend/cms/package.json ./cms/
# install and build the packages
RUN yarn install --production=false
COPY ./frontend/admin ./admin/
COPY ./frontend/ui ./ui/
WORKDIR ./ui/
RUN yarn build
WORKDIR ../admin/
RUN yarn build

FROM python:3.7.1-stretch
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y libpq-dev gcc ffmpeg libimage-exiftool-perl libvips-dev && \
    apt-get autoremove && \
    apt-get autoclean

# Create appropriate directories set env variables pointing to them
ENV DEBUG=False \
INCOMING_FILES_ROOT=/archive/incoming \
HAV_ARCHIVE_PATH=/archive/hav \
WHAV_ARCHIVE_PATH=/archive/whav \
WEBASSET_ROOT=/archive/webassets \
UPLOADS_ROOT=/archive/uploads \
DJANGO_MEDIA_ROOT=/archive/uploads \
DJANGO_SECRET_KEY=I_AM_VERY_UNSAFE \
IMAGINARY_SECRET=UNSAFE

RUN ["mkdir", "-p", "/archive/incoming", "/archive/hav", "/archive/whav", "/archive/webassets/", "/archive/uploads"]


RUN pip install -U pipenv

WORKDIR /hav/frontend
COPY --from=build-stage /code/admin/build ./admin/build

WORKDIR /hav/backend
COPY backend/Pipfile backend/Pipfile.lock ./

RUN pipenv install --system && pipenv install --system --dev

# Copy all backend files
COPY ./backend .

RUN ["python", "manage.py", "collectstatic", "--no-input"]

WORKDIR /hav

CMD ["daphne", "-p", "8000",  "-b", "0.0.0.0",  "hav.asgi:application"]
