#!/usr/bin/env bash
# author: bing

python -m rasa_core.run -d models/dialogue -u CriminalMiner/nlu --port 5002 --credentials credentials.yml --cors * --endpoints endpoints.yml
