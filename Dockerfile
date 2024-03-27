FROM python

LABEL maintainer = "Harshit M"
LABEL org.opencontainers.image.source = "https://github.com/djharshit/user-backend"

WORKDIR /home/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]
