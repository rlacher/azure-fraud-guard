# SPDX-License-Identifier: MIT
# Copyright (c) 2025 René Lacher

FROM python:3.12-slim

ARG DATA_FILENAME
ENV DATA_FILENAME=${DATA_FILENAME}

WORKDIR /data

COPY producer.py \
     requirements.txt \
     download.py ./

RUN pip3 install --no-cache-dir \
    -r requirements.txt

RUN test -n "$DATA_FILENAME"

RUN python3 download.py

CMD ["python3", "producer.py"]
