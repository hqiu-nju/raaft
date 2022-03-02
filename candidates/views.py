from django.shortcuts import render
# from .models import TransientEntry
# Create your views here.
from django.template import loader
from django.http import HttpResponse,Http404, HttpRequest
import json
from candidates.models import *
from django.utils import timezone
from django.core.files.storage import default_storage
import base64
import os
from decouple import config
import jsonloader
### import SLACK_WEBHOOK for channel
SLACK_WEBHOOK=config("SLACK_WEBHOOK")
def Index(request):
    latest_question_list = TransientEntry.objects.order_by('-pub_date')[:100]
    template = loader.get_template('candidates/index.html')
    context = {
        'FRB_info': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def Detail(request, question_id):
    try:
        question = TransientEntry.objects.get(id=question_id)
    except question.DoesNotExist:
        raise Http404("Transient entry does not exist")
    # verify=question.verification_set.order_by('-pub_date')[:1]
    return render(request, 'candidates/detail.html', {'question': question})

# def info(request, question_id):
#     try:
#         question = TransientEntry.objects.get(pk=question_id)
#     except TransientEntry.DoesNotExist:
#         raise Http404("Transient entry does not exist")
#     template = loader.get_template('candidates/info.html')
#     context={'question':question}
#     return HttpResponse(template.render(context, request))

def AddCandidate(request):
    if 'application/json' in request.META['CONTENT_TYPE']:
        #print ('hi')
        data = json.loads(request.body)
        #frb = data.get('TransientEntry', None)
        print("received",data["pub_date"])
        # newfrb = {'name':'test',
        #     'sn':37.1,
        #     'dm':1342,
        #     'boxcar':1,
        #     'latency':400.,
        #     'pub_date':str(datetime.datetime.now(pytz.UTC))[:-6],
        #     "beam":0,
        #     "mjd":500,
        #     }


        newfrb=TransientEntry(name=data["name"],
        pub_date=timezone.now(),
        beam=data["beam"],dm=data['dm'],sn=data['sn'],boxcar=data['boxcar'],width_value=data['boxcar'],
        mjd=data['mjd'],latency_ms=data['latency']
        )
        #,latestverify='',
        #frb_name.objects.create()
        newfrb.save()
        return HttpResponse("Success")


def Veto(request):
    if 'application/json' in request.META['CONTENT_TYPE']:
        data = json.loads(request.body)
        #frb = data.get('frb_name', None)
        print("received",data["pub_date"])
        new_veto=Veto(frb=TransientEntry.objects.get(name=data['name']),pub_date=timezone.now(),
        verify=data['verify'],reason=data['reason'],
        username=data['username']
        )
        new_veto.save()
        #frb_name.objects.create()
        return HttpResponse("Veto info added")

def MMAUpdates(request):
    if 'application/json' in request.META['CONTENT_TYPE']:
        data = json.loads(request.body)
        #frb = data.get('frb_name', None)
        print("received",data["pub_date"])
        imb64=data['payload']
        print(imb64[0])
        filename=str(imb64[0])
        payload=base64.b64decode(imb64[1])
        storepath=f"{default_storage.base_location}/{data['name']}"
        if os.path.exists(storepath):
            pass
        else:
            print(f"creating directory for {data['name']}")
            os.makedirs(storepath)
        with default_storage.open(f"{data['name']}/{filename}", 'wb+') as destination:
            destination.write(bytearray(payload))
            destination.close()
        newobject=Multimessenger(frb=TransientEntry.objects.get(name=data['name']),
        pub_date=timezone.now(),
        username=data['username'],
        choice_text=data['choice_text'],
        ra=data['ra'],
        dec=data['dec'],
        ra_err=data['ra_err'],
        dec_err=data['dec_err'],
        upload=f"{data['name']}/{filename}",
        )
        newobject.save()
        return HttpResponse("New counterpart added")
def Slack(request):
    # read slack interactive messages
    # print(str(request.body))
    # print(str(request.META['CONTENT_TYPE']))
    response={
            	"blocks": [
            		{
            			"type": "context",
            			"elements": [
            				{
            					"type": "plain_text",
            					"text": "Interaction received",
            					"emoji": True
            				}
            			]
            		}
            	]
            }
    if 'x-www-form-urlencoded' in request.META['CONTENT_TYPE']:
        data = json.loads(request.POST['payload'])
        user=data['user']['username']
        print(f"{user} sent the message through slack!")
        # print(data['message']['blocks'][1]['text']['text'])
        frbname=data['message']['blocks'][1]['text']['text']
        # entry=TransientEntry.objects.get(name=frbname)
        print(frbname)
        # print(TransientEntry.objects.get(name=frbname))
        if data["actions"][0]['action_id']=='actionId-0':
            # print('veto!')

            response['blocks'].append(
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": "Veto applied",
                        "emoji": True
                    }
                ]
            }
            )
            # new_veto=Veto(frb = entry,
            # pub_date=timezone.now(),
            # verify="1",reason="slack visual check",
            # username=user
            # )
            # new_veto.save()
        else:
            response['blocks'].append(
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": "Veto rejected",
                        "emoji": True
                    }
                ]
            }
            )
        jsonloader.poster(SLACK_WEBHOOK,response)

    return HttpResponse('Success')
