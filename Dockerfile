FROM node:24-alpine AS frontend
WORKDIR /app
COPY ml-system-app/package*.json ./
RUN npm install
COPY ml-system-app/ ./
RUN npm run build

FROM python:3.12
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py train.py ./
COPY --from=frontend /app/dist/ml-system-app/browser ./static
COPY docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh
VOLUME ["/app/mlruns", "/app/evaluation"]
EXPOSE 8000
CMD ["./docker-entrypoint.sh"]
