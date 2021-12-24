FROM python:3.10-slim

RUN apt-get update \
    && apt-get install build-essential libcurl4-gnutls-dev git -y

WORKDIR /eggnog

# build eggnog (https://github.com/breakthatbass/eggnog)
RUN git clone https://github.com/breakthatbass/eggnog.git \
    && cd eggnog \
    && NOG_INSTALL_PATH=/usr/local/bin make install

WORKDIR /workdir

CMD [ "python3" ]
