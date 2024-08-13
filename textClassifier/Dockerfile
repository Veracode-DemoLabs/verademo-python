FROM python:3.12.3

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt && apt update && apt-get install -y iputils-ping 

COPY . .

EXPOSE 3306

CMD ["python", "server.py"]
