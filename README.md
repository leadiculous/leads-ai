# leads-ai

## Installation

```bash
$ pip install -r requirements.txt
```

## Protocol Buffers

To compile the protocol buffers, run the build script:

```bash
$ ./build.sh
```

## Docker
To build and run the Docker container, run the following commands:

```bash
$ docker build -t leads-ai .
$ docker run -d -p 127.0.0.1:50051:50051 --name leads-ai leads-ai
```
