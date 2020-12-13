FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /home/backend
WORKDIR /home/backend
COPY backend /home/backend
RUN pip install -r requirements.txt
