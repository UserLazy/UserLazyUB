# Using Python Slim-Buster
FROM biansepang/weebproject:buster


RUN git clone -b master https://github.com/UserLazy/UserLazyUB.git /home/weebproject/ \
    && pip3 install --no-cache-dir -r home/weebproject/requirements.txt \
    && chmod 777 /home/weebproject \
    && mkdir /home/weebproject/bin/


# Copies config.env (if exists)
COPY ./sample_config.env ./config.env* /home/weebproject/

# changing workdir
WORKDIR /home/weebproject/

# Finalization
CMD ["python3","-m","userbot"]
