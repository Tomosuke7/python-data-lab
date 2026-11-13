FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    streamlit \
    pandas \
    numpy \
    matplotlib \
    seaborn \
    scipy \
    openpyxl

EXPOSE 8501

CMD ["streamlit", "run", "app.py", \
     "--server.address=0.0.0.0"]
