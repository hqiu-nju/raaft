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
### a test run code that sends snoopy and other test images to the django sql server via json httppost

def _main():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description='Script description', formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Be verbose')
    parser.add_argument('-u', '--url',type=str, help='url address',default = "http://127.0.0.1:8000/candidates/")
    parser.add_argument('-n', '--name',type=str, help='frb name, keep none for autogeneration',default = None)
    parser.add_argument(dest='files', nargs='+')
    parser.set_defaults(verbose=False)
    values = parser.parse_args()
    if values.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    url=values.url
    fname=values.files[0]
    #print(values.files[0])
    if values.name is None:
        frb=datetime.datetime.now(pytz.UTC).strftime("%y%m%d_t%H") ### automatically creates name for frb
    else:
        frb=values.name
    newfrb=snoopy2dict(fname,frb)
    print("Sending "+frb)
    print(newfrb)
    httppost(url+"newcand/",newfrb)
    testimage_dir='pulsarcheck.png'
    testimage_name='foundpulsar.png'
    testfits_dir='frb21451_n1e4_15min.fits'
    testfits_name='frb21451.fits'
    f=open(testfits_dir,'rb')
    im_bytes = f.read()
    im_b64 = base64.b64encode(im_bytes).decode("utf8")
    newmma = { 'name':frb,
    'pub_date':str(datetime.datetime.now(pytz.UTC))[:-6],
    'choice_text':"this is a counterpart",
    'username':"raaftbot",
    'ra':200,
    'dec':200,
    'ra_err':1,
    'dec_err':1,
    'payload':(testfits_name,im_b64),
    }
    httppost(url+"mma/",newmma)
    f.close()

def snoopy2dict(snoopyfile,frb):
    """
    reads a snoopy file and turns it into dictionary
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
    vetos={'name':frb,
    'verify':choice,
    'reason':reason,
    'username':username,
    }
def httppost(url,jsonfile):
    headers = {'content-type': 'application/json'}
    r=requests.post(url, data=json.dumps(jsonfile), headers=headers)
    print(r.text)


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


"""


if __name__ == '__main__':
    _main()
