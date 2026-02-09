#!/bin/bash

GIT_MESSAGE="${1:-.}"

git add .
git commit -m "$GIT_MESSAGE"
git push
git status

exit
