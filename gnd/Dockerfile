FROM eclipse-temurin:21-jre-alpine AS builder

LABEL maintainer="cmahnke@gmail.com"
LABEL org.opencontainers.image.source=https://github.com/cmahnke/data-containers

# Latest Jena: https://dlcdn.apache.org/jena/binaries/apache-jena-5.0.0.tar.gz
# Latest Fuseki: https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-5.0.0.tar.gz
# Old releases: https://archive.apache.org/dist/jena/binaries/

ENV JENA_DOWNLOAD_URL=https://archive.apache.org/dist/jena/binaries/apache-jena-4.9.0.tar.gz \
    FUSEKI_DOWNLOAD_URL=https://archive.apache.org/dist/jena/binaries/apache-jena-fuseki-4.9.0.tar.gz \
    HDT_DOWNLOAD_URL=https://github.com/rdfhdt/hdt-java/releases/download/v3.0.10/rdfhdt.tar.gz \
    BUILD_DIR=/tmp/build \
    JENA_HOME=/opt/jena \
    FUSEKI_HOME=/opt/fuseki \
# Make sure ènvsubst`is present
    RUN_DEPS="gettext" \
    BUILD_DEPS=""

RUN --mount=target=/mnt/build-context \
    apk --update upgrade && \
    apk add --no-cache $RUN_DEPS $BUILD_DEPS && \
    mkdir -p $BUILD_DIR $JENA_HOME $FUSEKI_HOME/run/extra && \
    wget -O `basename $JENA_DOWNLOAD_URL` "$JENA_DOWNLOAD_URL" && \
    tar xzf `basename $JENA_DOWNLOAD_URL` && \
    rm -rf apache-jena-*/lib-src apache-jena-*/src-examples apache-jena-*/bat && \
    cp -r apache-jena-*/* $JENA_HOME/ && \
    rm -rf cp apache-jena-* && \
    wget -O `basename $FUSEKI_DOWNLOAD_URL` "$FUSEKI_DOWNLOAD_URL" && \
    tar xzf `basename $FUSEKI_DOWNLOAD_URL` && \
    cp -r apache-jena-fuseki*/* $FUSEKI_HOME/ && \
    wget -O `basename $HDT_DOWNLOAD_URL` "$HDT_DOWNLOAD_URL" && \
    tar xzf `basename $HDT_DOWNLOAD_URL` && \
    cp hdt-java-package-*/lib/hdt-*.jar $FUSEKI_HOME/run/extra && \
    rm $FUSEKI_HOME/run/extra/hdt-java-cli-*.jar

FROM alpine:3.19

ENV GND_URL=https://data.dnb.de/opendata/authorities-gnd_lds.hdt.gz \
    JENA_HOME=/opt/jena \
    FUSEKI_HOME=/opt/fuseki \
    RUN_DEPS="gettext openjdk17-jre curl bash procps pwgen" \
    JENA_USER=jena \
    DATASET=gnd \
    TDB_VERSION=tdb2 \
    FUSEKI_ADMIN_PASSWORD=setup \
    FUSEKI_CLASSES="run/extra/hdt-jena-3.0.10.jar:run/extra/hdt-java-core-3.0.10.jar:run/extra/hdt-api-3.0.10.jar" \
    IMPORT_DIR=/tmp/import \
    JAVA_OPTIONS="-Xmx4096M"

COPY --from=builder $JENA_HOME $JENA_HOME
COPY --from=builder $FUSEKI_HOME $FUSEKI_HOME

RUN --mount=target=/mnt/build-context \
    apk --update upgrade && \
    apk add --no-cache $RUN_DEPS && \
    mkdir -p /entrypoint.d/ $FUSEKI_HOME/run/configuration $FUSEKI_HOME/run/data $IMPORT_DIR && \
    addgroup -g 1000 $JENA_USER && \
    adduser -D -u 1000 -G $JENA_USER $JENA_USER && \
    cp /mnt/build-context/gnd/conf/shiro.ini $FUSEKI_HOME/shiro.ini.template &&\
    cp /mnt/build-context/gnd/conf/config.ttl $FUSEKI_HOME/run/config.ttl &&\
    cp /mnt/build-context/gnd/scripts/entrypoint.sh /entrypoint.d/ && \
    envsubst '${FUSEKI_ADMIN_PASSWORD}' < "$FUSEKI_HOME/shiro.ini.template" > "$FUSEKI_HOME/run/shiro.ini" && \
    wget -O /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/81b1373f17855a4dc21156cfe1694c31d7d1792e/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it.sh && \
    cd $IMPORT_DIR && \
    wget -O `basename $GND_URL` $GND_URL && \
    gunzip `basename $GND_URL` && \
    mv authorities-gnd_lds.hdt $FUSEKI_HOME/run/data/ && \
    cd $FUSEKI_HOME && \
    #sed -E -i  "s/JAR=\"\"/JAR=\"$FUSEKI_CLASSES\"/g" $FUSEKI_HOME/fuseki-server && \
    # Start Fuseki as simple sanity check
    $FUSEKI_HOME/fuseki start && \
    /usr/local/bin/wait-for-it.sh -t 60 localhost:3030 && \
    #curl 'http://localhost:3030/$/datasets' -u admin:${FUSEKI_ADMIN_PASSWORD} -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' --data "dbName=${DATASET}&dbType=${TDB_VERSION}" && \
    #$FUSEKI_HOME/tdbloader --loc=$FUSEKI_HOME/run/databases/gnd /Users/cmahnke/projects/kustodie/data-containers/
    $FUSEKI_HOME/fuseki stop && \
    chown -R $JENA_USER:$JENA_USER $FUSEKI_HOME/run && \
# Cleanup
    rm -rf $IMPORT_DIR

WORKDIR $FUSEKI_HOME
ENTRYPOINT [ "/entrypoint.d/entrypoint.sh" ]
CMD ["./fuseki-server"]
EXPOSE 3030
VOLUME [ "/opt/fuseki/run" ]
USER $JENA_USER
