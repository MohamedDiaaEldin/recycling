#!/usr/bin/bash

git status 
git add .
read -p "enter commit message: " MESSAGE
git commit -m "$MESSAGE"
git push origin master
