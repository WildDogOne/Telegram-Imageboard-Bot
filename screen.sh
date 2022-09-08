#!/bin/bash
screen -dmS delishbot
screen -r -S delishbot -X stuff 'cd xxx/delishBotv2\n'
screen -r -S delishbot -X stuff 'python delishbotv2.py\n'

