#!/usr/bin/env bash
# author: Xu

python -m rasa_core.train -s data/weather_stories.md -d data/criminal_domain.yml -o models/dialogue  # --epochs 500 --nlu_threshold 0.4 --core_threshold 0.4