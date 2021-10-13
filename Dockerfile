FROM python:3.9-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update
RUN apt-get install -y openjdk-11-jre-headless
RUN apt-get install -y tcl

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

# Run the application:
CMD ["uvicorn", "main:app"]
