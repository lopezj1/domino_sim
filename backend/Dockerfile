FROM python:3.11-slim
WORKDIR /app
RUN pip install fastapi==0.109.0 "uvicorn[standard]==0.27.0" pydantic==2.5.0 numpy matplotlib
COPY src/ ./src/
EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
