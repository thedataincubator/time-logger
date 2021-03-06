#!/bin/bash
docker build -t logger .
docker run -it \
  -p 5000:5000 \
  -e PORT=5000 \
  -e SECRET_KEY="sup" \
  -e DATABASE_URL="sqlite:///test.db" \
  logger:latest /bin/bash -c "py.test"
