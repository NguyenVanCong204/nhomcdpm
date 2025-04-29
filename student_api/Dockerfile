FROM python:3.11.12-slim-bullseye
WORKDIR /api
COPY . /api
RUN pip install -r require.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]