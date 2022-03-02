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


def snoopy2dict(snoopyfile,frb):
    """
    reads a snoopy format file and turns it into dictionary, will need to handle string instead
    Parameters
    ----------
    snoopyfile : str
        name of file
    frb : str
        name of TransientEntry
    """
    data=np.genfromtxt(snoopyfile)

    # S/N, sampno, secs from file start, boxcar, idt, dm, beamno, mjd, latency_ms
    newfrb = {'name':frb,
        'sn':data[0],
        'dm':data[-4],
        'boxcar':data[3],
        'latency':data[-1],
        'pub_date':str(datetime.datetime.now(pytz.UTC))[:-6],
        "beam":data[-3],
        "mjd":data[-2],
        }
    return newfrb

def vetojson(frb,choice,reason='',username='raaftbot'):
    """Loading for the Veto entry.
    Parameters
    ----------
    name : str
        Entry name of transient, must match existing TransientEntry object
    verify : int
        Quick reference options are (0,"Unverified"),(1,'FRB'),(2,'Pulsar'),(-1,'RFI'),(3,'Unknown')
    reason : str
        Give a reason why!
    username : str
        Who sent this?
    """
    vetos={'name':frb,
    'verify':choice,
    'reason':reason,
    'username':username,
    }
    return vetos

def poster(url,jsonfile):
    """super vanilla json posting function for both django and slack
    Parameters
    ----------
    url : str
        URL for posting json, should be one of the views.py functions, the specific url should be in urls.py in the app folder
    jsonfile: dict
        json payload to send over
    """
    headers = {'content-type': 'application/json'}
    r=requests.post(url, data=json.dumps(jsonfile), headers=headers)
    print(r.text)

class SlackRaaft:
    def __init__(self,info,url):
        """initiate function for starting a slack upload with raaft.
        Parameters
        ----------
        info : dict
            a dictionary with snoopy detection data, format see snoopy2dict
        """
        self.name=info['name']
        # self.pub_date=info['pub_date'],
        # self.beam=info["beam"]
        # self.dm=info['dm']
        # self.sn=info['sn']
        # self.boxcar=info['boxcar']
        # self.width_value=info['boxcar']
        # self.mjd=info['mjd']
        # self.latency_ms=info['latency']
        self.snoopy2=info
        self.url=url
    def CreateVetoBlock(self,image="https://assets3.thrillist.com/v1/image/1682388/size/tl-horizontal_main.jpg"):
        """initiate function for starting a slack upload with raaft.
        Parameters
        ----------
        image : str
            url of image
        """
        payload = {
            	"blocks": [
            		{
            			"type": "header",
            			"text": {
            				"type": "plain_text",
            				"text": "New Candidate",
            				"emoji": True
            			}
            		},
            		{
            			"type": "header",
            			"text": {
            				"type": "plain_text",
            				"text": self.name,
            				"emoji": True
            			}
            		},
            		{
            			"type": "image",
            			"title": {
            				"type": "plain_text",
            				"text": "FRB waterfall",
            				"emoji": True
            			},
            			"image_url": "https://assets3.thrillist.com/v1/image/1682388/size/tl-horizontal_main.jpg",
            			"alt_text": "marg"
            		},
            		{
            			"type": "actions",
            			"elements": [
            				{
            					"type": "button",
            					"text": {
            						"type": "plain_text",
            						"text": "Confirm",
            						"emoji": True
            					},
            					"value": "click_me_123",
            					"action_id": "actionId-0"
            				},
            				{
            					"type": "button",
            					"text": {
            						"type": "plain_text",
            						"text": "False",
            						"emoji": True
            					},
            					"value": "click_me_123",
            					"action_id": "actionId-1"
            				}
            			]
            		}
            	]
            }
        # self.vetopayload=payload
        return payload
    def CreateCounterpartBlock(self,image):

        return payload

    def push(self,payload):
        poster(self.url,payload)



"""
    newfrb = {'name':'test',
        'sn':37.1,
        'dm':1342,
        'boxcar':1,
        'latency':400.,
        'pub_date':str(datetime.datetime.now(pytz.UTC))[:-6],
        "beam":0,
        "mjd":500,
        }
    newmma = { 'name':'test',
    'pub_date':str(datetime.datetime.now(pytz.UTC))[:-6],
    'choice_text':"this is a counterpart",
    'username':"raaftbot",
    'ra':200,
    'dec':200,
    'ra_err':1,
    'dec_err':1,
    }
    newvetp=

"""
