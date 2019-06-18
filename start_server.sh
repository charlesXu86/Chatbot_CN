#!/usr/bin/env bash

nohup python manage.py runserver 172.18.103.43:8008 > /home/souche/logs/chatbot_log 2>&1 &