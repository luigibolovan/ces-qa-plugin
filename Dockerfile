FROM python:latest

WORKDIR /sccwrapper

COPY runSCC.sh runSCC.sh
COPY bin/unix/* bin/unix/
COPY data/* data/
COPY src/* src/

ENTRYPOINT ["bash", "./runSCC.sh"]
