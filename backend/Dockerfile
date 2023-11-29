FROM python:3.9.12

WORKDIR /app

COPY . .

# RUN pip install --upgrade pip
RUN pip install flask
# RUN pip install requests
RUN pip install psycopg2

EXPOSE 5555

CMD ["python3", "webapp.py"]