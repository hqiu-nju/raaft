import requests
import json
import pytz
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import logging
### a simple code that sends snoopy to the django sql server via json httppost

def _main():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description='Script description', formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Be verbose')
    parser.add_argument('-u', '--url',type=str, help='url address',default = "http://127.0.0.1:8000/candidates/newcand/")
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
    httppost(url,newfrb)

    # data = {
    #         {'frb_name':'val1'},
    #         {'pub_date':str(datetime.datetime.now(pytz.UTC))[:-6]},
    #         {'sn_value':1},
    #         {'dm_value':1},
    #         {'width_value':1},
    #         {'latency_ms':10},
    #         {'mjd':10000},
    #         {'beam':1},
    #         }
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
"""


if __name__ == '__main__':
    _main()
