FROM python:3.12-slim

WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# compile proto files
COPY protos ./protos
COPY build.sh .
RUN ./build.sh

# copy app
COPY . .

# expose GRPC port
EXPOSE 50051

ENTRYPOINT ["python", "main.py"]
