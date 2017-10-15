#!/bin/sh
case "$OSTYPE" in
  solaris*) echo "SOLARIS" ;;
  darwin*)  killall -9 mongod;;
  linux*)   echo "LINUX" ;;
  bsd*)     echo "BSD" ;;
  msys*)    taskkill /f /im mongod;;
  *)        echo "unknown: $OSTYPE" ;;
esac
mongod --dbpath mongodb/db/data
