#!/bin/sh

cd hq

rq-dashboard -p 9181 -u 'redis://redis/0'
