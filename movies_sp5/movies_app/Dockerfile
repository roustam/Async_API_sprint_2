FROM python:3.10
WORKDIR /opt/app
COPY requirements.txt requirements.txt

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain nightly
ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
    

CMD ["sh", "run_app.sh"]