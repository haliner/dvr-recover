#!/bin/sh
set -e

find -name '*.java' -print0 | xargs -0 sed -i -e 's/^[ \t]*$//'
