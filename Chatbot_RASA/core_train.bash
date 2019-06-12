#!/usr/bin/env bash
# author: bing

python -m rasa_core.train -s data/stories.md -d data/criminal_domain.yml -o models/dialogue