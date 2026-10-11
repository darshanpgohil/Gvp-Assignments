#!/bin/bash

read -p "Enter The Directory Path : " dir

if [ -d "$dir" ];
then
       datetime=$(date +"%Y-%m-%d %H-%M-%S")

       backup="$backup_$datetime.tar.gz"

       tar -czf "$backup" "$dir"

       echo "$backup File Created Successfully"
else
       echo "$dir Not Exiest"
fi
