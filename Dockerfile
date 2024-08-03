FROM python:3.12

.dockerignore __pycache__/

ADD * /app/
RUN pip install -r /app/requirements.txt
CMD ["python3", "/app/controller.py"]