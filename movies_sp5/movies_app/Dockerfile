FROM python:3.10
WORKDIR /opt/app/src
COPY requirements.txt requirements.txt

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain nightly
ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
    

CMD ["gunicorn", "main:app", "--workers 4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind"," 0.0.0.0:80"]