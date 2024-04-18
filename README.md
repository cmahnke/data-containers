Data containers
===============


# GeoNames

This image provides a [Solr](https://solr.apache.org/) instance containing all information from [GeoNames](https://www.geonames.org/). Have a look at the [schema](./geonames/schema.json) to get an idea of the available fields.

## Building

```
docker build -f geonames/Dockerfile -t ghcr.io/cmahnke/data-containers/geonames .
```

## Running

Make sure to expose the Solr port (8983) to be able to use the container.

```
docker run -p 8983:8983 -it ghcr.io/cmahnke/data-containers/geonames 
```

## Using

After starting the container you can use curl to query for a place name.

```
curl http://localhost:8983/solr/geonames/query?debug=query&q=n:G%C3%B6ttingen
```

You can also combine different parameters fo a search, a noteable example is to limit results to a bounding box of geo coordinates.

# GND

## Building

```
docker buildx build --progress=plain -f gnd/Dockerfile . -t ghcr.io/cmahnke/data-containers/gnd:latest
```

## Running

Make sure to expose the Fuseki port (3030) to be able to use the container.

```
docker run -it -p3030:3030  ghcr.io/cmahnke/data-containers/gnd:latest /bin/sh
```

## Using

http://localhost:3030/#/dataset/gnd/query