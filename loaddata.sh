#!/bin/bash

i=1
while [ "$i" -le 822 ]; do
    python manage.py loaddata community_data/data-$i.json
    # sleep 3
    if [ $? -eq 0 ]; then
        echo [Success] Load data-$i
        i=$(( i + 1 ))
    else
        echo [FAIL]
        break
    fi    
done 