#!/bin/bash

for ((i=1; i<=776; i++)); do
    python manage.py loaddata movies_data/data-$i.json
    sleep 5
done
