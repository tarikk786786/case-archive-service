FROM python:3.12-alpine
WORKDIR /app
COPY main.py .
ENV PORT=10000
ENV RATE_LIMIT_KBPS=200
EXPOSE 10000
CMD ["python", "main.py"]
