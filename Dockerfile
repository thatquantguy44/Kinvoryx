FROM python:3.11-slim

WORKDIR /app

COPY src/ src/
COPY examples/ examples/

ENV PORT=8080
EXPOSE 8080

CMD ["python", "examples/demo/optimizer_form_server.py"]
