FROM python:latest

WORKDIR /repo

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY Subscriber_module.py /repo

CMD [ "python", "-u", "./Subscriber_module.py" ]
