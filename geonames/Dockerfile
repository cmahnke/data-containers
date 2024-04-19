FROM solr:9.5-slim

LABEL maintainer="cmahnke@gmail.com"
LABEL org.opencontainers.image.source=https://github.com/cmahnke/data-containers

USER root

ENV GEONAMES_ALL_COUNTRIES="http://download.geonames.org/export/dump/allCountries.zip" \
    REQ_BUILD="python3 unzip" \
    BUILD_CONTEXT=/mnt/build-context \
    DIR_BUILD=./geonames-data \
    JSON_SCHEMA=schema.json

RUN --mount=target=/mnt/build-context \
    apt-get -yqq update && \
    apt-get install --assume-yes --no-install-recommends ${REQ_BUILD} busybox curl && \
# Copy helper script
    mkdir -p $DIR_BUILD $SOLR_HOME && \
    cp $BUILD_CONTEXT/geonames/jsonify.py $BUILD_CONTEXT/geonames/$JSON_SCHEMA $DIR_BUILD/ && \
# Download data files
    cd $DIR_BUILD && \
    wget -qO- "$GEONAMES_ALL_COUNTRIES" | zcat | python3 jsonify.py -g - > $(basename $GEONAMES_ALL_COUNTRIES .zip).json && \
# Create Solr core
    cd /opt/solr && \
    bin/solr start -force && bin/solr create -force -c geonames && \
# Setup schema
    bin/solr config -solrUrl http://localhost:8983/solr/ -c geonames -p 8983 -action set-user-property -property update.autoCreateFields -value false && \
    cd $DIR_BUILD && \
    echo "Adding schema from $JSON_SCHEMA" && \
    curl http://0.0.0.0:8983/api/cores/geonames/schema -X POST -H 'Content-type:application/json' --data-binary @$JSON_SCHEMA && \
# Import of 'allCountries.json'
    echo "Importing data from $(basename $GEONAMES_ALL_COUNTRIES .zip).json" && \
    curl -X POST -H 'Content-type:application/json' -T$(basename $GEONAMES_ALL_COUNTRIES .zip).json 'http://0.0.0.0:8983/solr/geonames/update/json/docs?split=/&f=id:/id&f=name:/name&f=uri:/uri&f=alternatename:/alternatename&f=coordinate:/coordinate&f=featureclass:/featureclass&f=featurecode:/featurecode&f=country:/country&f=population:/population&f=elevation:/elevation&f=timezone:/timezone&commit=true&optimize=true' && \
# Set permissons
    chown -R $SOLR_USER /var/solr && \
## Cleanup
    rm -f $(basename $GEONAMES_ALL_COUNTRIES .zip).json && \
    cd /opt/solr && \
    rm -rf $DIR_BUILD && \
    apt-get --purge remove -y ${REQ_BUILD} && \
    apt-get autoremove -fy && apt-get clean && apt-get autoclean -y && \
	rm -rf /var/lib/apt/lists/*

USER $SOLR_USER

VOLUME /var/solr

EXPOSE 8983
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["solr-foreground"]