FROM python:3.10

WORKDIR /app

# Copy everything from the current directory (which is ./dashboard) to /app in the container
COPY . /app

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "app.py"]
