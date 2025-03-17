FROM python:3.10-slim
COPY . /grep-ast

# Unfortunately to build the multi-arch docker image we need `build-essential` for amd64.
# Apparently py-tree-sitter-languages doesn't have a pre-built binary wheel?

RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential git libportaudio2 && \
    rm -rf /var/lib/apt/lists/* && \
    pip install pytest && \
    pip install --no-cache-dir /grep-ast
WORKDIR /app
ENTRYPOINT ["grep-ast"]
