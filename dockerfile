FROM python:3.10-slim

COPY app /app

EXPOSE 8080

CMD ["python", "app/solution.py"]
