#!/bin/sh
mkdir -p posts flags
while true; do NODE_PATH=. ./node blogger.js; done
