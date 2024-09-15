#!/bin/bash

openssl rand -base64 756 > /opt/keyfile/mongo-keyfile

chmod 400 /opt/keyfile/mongo-keyfile
chown mongodb:mongodb /opt/keyfile/mongo-keyfile
