import jsonloader
import requests
import json
import pytz
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import logging
import base64

"""
A package for organising raaft json posts to raaft and slack
"""

from decouple import config
### import SLACK_WEBHOOK for channel
SLACK_WEBHOOK=config("SLACK_WEBHOOK")


newfrb=jsonloader.snoopy2dict("testsnoopy.txt",'test_entry_2022')
newnote=jsonloader.SlackRaaft(newfrb,SLACK_WEBHOOK)

blocks=newnote.CreateVetoBlock()
push=newnote.push(blocks)
