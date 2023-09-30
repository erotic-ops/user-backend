FROM python

WORKDIR /home/app/server

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "server.py"]
