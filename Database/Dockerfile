FROM mariadb:latest

COPY VerifiedPairs.csv /home/
COPY setup.sql.zip /home/
COPY init-example-databases.sh /home/

RUN curl -sL https://deb.nodesource.com/setup | bash - && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN chmod 700 /home/init-example-databases.sh
