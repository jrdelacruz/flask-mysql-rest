FROM python:3.12.2
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=app.py
CMD ["sh", "-c", "flask run --host=0.0.0.0"]