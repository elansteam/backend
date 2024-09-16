#!/bin/bash

set -e

(
    while true; do
        {
            mongosh --eval "" &&
            break
        } || {
            echo "Waiting for connection..."
            sleep 1
        }
    done
    echo "Connected"

    while true; do
        echo "Initiating replica set..."
        result=$(mongosh --eval "rs.initiate({_id: 'rs0', members: [{ _id: 0, host: '${MONGODB_HOSTNAME}:27017' }]})")
        if [ "$result" == "{ ok: 1 }" ]; then
            echo "Success"
            break
        else
            echo "Error. Retrying..."
            sleep 1
        fi
    done

    create_users="
    while (true) {
        try {
            var adminDB = db.getSiblingDB('${INITDB_ROOT_DATABASE}');
            adminDB.createUser({user: '${INITDB_ROOT_USERNAME}', pwd: '${INITDB_ROOT_PASSWORD}', roles: [{ role: 'root', db: 'admin' }]});
            break;
        } catch {
            console.log('Waiting for initalization...')
            sleep(1000);
        }
    }
    console.log('Admin created successfully');

    adminDB.auth('${INITDB_ROOT_USERNAME}', '${INITDB_ROOT_PASSWORD}');
    var dbName = db.getSiblingDB('${COMMON_DATABASE}');

    adminDB.createUser({
        user: '${COMMON_USERNAME}',
        pwd: '${COMMON_PASSWORD}',
        roles: [{ role: 'readWrite', db: '${COMMON_DATABASE}' }]
    });

    console.log('Common user created successfully');
    "

    mongosh --eval "$create_users"
) &
