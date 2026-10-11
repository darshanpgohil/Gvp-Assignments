#!/bin/bash

read -p "Enter The Directory Path : " dir

if [ -d "$dir" ];
then
       datetime=$(date +"%Y-%m-%d %H-%M-%S")

       backup="$(backup_datetime)"

       tar -zcf "$backup" "$dir"

       echo "$backup File Created Successfully"
else
       echo "$dir Not Exiest"
fi
