#!/bin/sh

if [ -z "$FUSEKI_ADMIN_PASSWORD" ] ; then
    FUSEKI_ADMIN_PASSWORD=`pwgen -n 10 1`
    echo "Generated password $FUSEKI_ADMIN_PASSWORD"
fi

envsubst '${FUSEKI_ADMIN_PASSWORD}' < "$FUSEKI_HOME/shiro.ini.template" > "$FUSEKI_HOME/run/shiro.ini"
unset FUSEKI_ADMIN_PASSWORD

exec "$@"