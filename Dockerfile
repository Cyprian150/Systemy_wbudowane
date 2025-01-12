FROM python:latest

WORKDIR /repo

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY API_module_test.py /repo

CMD [ "python", "-u", "./API_module_test.py" ]
#ENTRYPOINT [ "python", "./API_module_test.py" ]
