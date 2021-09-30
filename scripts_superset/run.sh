#!/usr/bin/env bash


# initialise superset

#superset fab create-admin --username adminnew --firstname Superset --lastname Admin --email admin@superset.com --password admin

superset db upgrade

superset init