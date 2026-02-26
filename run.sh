#!/bin/bash

# Define a variable named 'NOW' with the current date and time
NOW=$(date +"%Y-%m-%d_%H-%M-%S")

python landmass_areas/landmass_areas.py > landmass_areas/outputs/logs/log_$NOW.txt