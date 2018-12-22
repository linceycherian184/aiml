#!/bin/bash
[ -z "$1" ] && exit 1
curl -i -X POST --data '{"msg":"'"$*"'"}' localhost:8765
