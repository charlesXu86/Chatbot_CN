#!/usr/bin/env bash
# author: bing

python -m rasa_core.train interactive -s data/stories.md -d data/criminal_domain.yml --nlu CriminalMiner/nlu -o models/dialogue --endpoints endpoints.yml