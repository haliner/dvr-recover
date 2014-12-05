#!/bin/sh

find '(' -name '*.c' -o -name '*.h' ')' -print0 | xargs -0 wc
