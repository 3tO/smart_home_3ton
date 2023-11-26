from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import View
import time as ttime
from datetime import datetime
from datetime import timedelta
from pytz import UTC
from django.views.decorators.csrf import csrf_protect
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

def home(request, quantity=24):

    def get_list_values(topic):
        
        v = list(Values.objects.filter(topic__name=topic,
            date_pub__gte=last_date-timedelta(minutes=minutes_set), date_pub__lte=last_date)
            .values_list('value', 'date_pub').order_by('-date_pub'))
        return v

    def get_piont_value(val, i):

        if i <= len(val)-1 and val[i][1] > last_date - timedelta(minutes=5*n, seconds=150) \
                          and val[i][1] < last_date - timedelta(minutes=5*n, seconds=-149):
            w = float(val[i][0])
            if len(val)-1 > i:
                i += 1
        else:
            w = 'None' if n!=time_point-1 else float(val[i][0]) if len(val)!=0  else 20
        return w, i
        
    minutes_set = quantity * 60
    last_date = max(
                Values.objects.filter(topic__name='/outside/temp').last().date_pub,
                Values.objects.filter(topic__name='/basement/kotel/water').last().date_pub,
                Values.objects.filter(topic__name='/basement/kotel/smoke').last().date_pub,
        )
    print(" view_now_date:", datetime.now())
    print("view_last_date:", last_date, "\n")

    water = get_list_values('/basement/kotel/water')
    smoke = get_list_values('/basement/kotel/smoke')
    outside_temp = get_list_values('/outside/temp')


    data_all = []
    i, j, m = 0, 0, 0
    time_point = quantity * 12 + 1
    for n in range(time_point):
        w, i = get_piont_value(water, i)
        s, j = get_piont_value(smoke, j)
        o, m = get_piont_value(outside_temp, m)

        data_all.append([
                'Date('+str(int(ttime.mktime((last_date - timedelta(minutes=5*n)).timetuple()))*1000)+')',
                o,
                str((last_date - timedelta(minutes=5*n)).strftime("%b %d, %H:%M"))+"\noutside: " + str(o),
                w,
                str((last_date - timedelta(minutes=5*n)).strftime("%b %d, %H:%M"))+"\nwater: " + str(w),
                s,
                str((last_date - timedelta(minutes=5*n)).strftime("%b %d, %H:%M"))+"\nsmoke: " + str(s)
                ])
            
    data_all = [
                    [{'type': 'date', 'label': 'Date'}, 
                    'temp', 
                    {'type':'string','role':'tooltip'}, #,'p': {'html': 'true'}},
                    'water',
                    {'type':'string','role':'tooltip'},
                    'smoke',
                    {'type':'string','role':'tooltip'},
                    ]
                ] + data_all[::-1]

    status = UTC.localize(datetime.now() - timedelta(minutes=5)) < last_date 

    context = {'data_all' : data_all,
                'status' : status,
                }
    return render(request, 'mqtt/charts.html', context=context)

class htc_merge(View):
    """docstring for htc"""
    def get(self, request):
        temps = [Values.objects.filter(topic__name='/basement/kotel/water').values('date_pub').last()['date_pub'].strftime("%b %d, %H:%M:%S"),
                 Values.objects.filter(topic__name='/basement/kotel/water').values('value').last()['value'],
                 Values.objects.filter(topic__name='/basement/kotel/smoke').values('value').last()['value'],
                 Values.objects.filter(topic__name='/outside/temp').values('value').last()['value'],
                ]
        status = UTC.localize(datetime.now() - timedelta(minutes=5)) < Values.objects.all().values('date_pub').last()['date_pub']
        context = {'temps':temps,
                    'status' : status,}
        return render(request, 'mqtt/htc_merge.html', context=context)

class htc_ajax(View):
    """docstring for htc"""
    def get(self, request):
        if request.is_ajax():
            
            def get_last_date(topics):
                all_date = []
                for topic in topics:
                    if Topic.objects.filter(name=topic).exists(): 
                        all_date.append(Values.objects.filter(topic__name=topic).last().date_pub)

                all_date = max(all_date) if all_date else None

                    
                return all_date

            last_date = get_last_date(['/outside/temp','/basement/kotel/water', '/basement/kotel/smoke'])
            
            if not last_date:
                context = {
                            'success' : True,
                            'water' : 'Немає данних',
                            'status' : False,}
                return JsonResponse(context)
            

            if str(request.GET.get('time')) < datetime.strftime(last_date, "%b %d, %H:%M:%S"):

                def get_valueX(value, topic):
                    last_temp = Values.objects.filter(topic__name=topic) \
                                        .values('value', 'date_pub').last()
                    try:
                        old_temp = float(request.GET.get(value+'_old')[0:-2])
                        temp = float(last_temp['value']) if last_temp['date_pub'] > last_date \
                                                        - timedelta(seconds=25) else '------'
                        
                        temp = str(temp) + ' &#8593' if temp > old_temp else str(temp) \
                                        + ' &#8595' if temp < old_temp else str(temp) + '&ensp;'*2
                    except:
                        temp = str(last_temp['value'])+'&ensp;'*2 if last_temp['date_pub'] > \
                                                    last_date - timedelta(seconds=25) else \
                                                    '------' + '&ensp;'*2

                    return temp

                def get_value(topic):
                    data = Values.objects.filter(topic__name=topic) \
                        .values('value', 'date_pub').order_by('-date_pub')[:2]

                    if data[0]['date_pub'] > last_date - timedelta(seconds=25):

                        if float(data[0]['value']) > float(data[1]['value']):
                            res = str("{:.2f}".format(float(data[0]['value']))) + ' &#8593' 
                        
                        elif float(data[0]['value']) < float(data[1]['value']) :
                            res = str("{:.2f}".format(float(data[0]['value']))) + ' &#8595' 
                        
                        else:
                            res = str("{:.2f}".format(float(data[0]['value']))) + '&ensp;'*2
                        # res
                    else:
                        res =  '------'  + '&ensp;'*2
                    return res

                water = get_value('/basement/kotel/water')
                smoke = get_value('/basement/kotel/smoke')
                outside_temp = get_value('/outside/temp')



                status = UTC.localize(datetime.now() - timedelta(minutes=5)) < last_date
                context = {
                            'success' : True,
                            'last_date' : last_date.strftime("%b %d, %H:%M:%S"),
                            'water' : water,
                            'smoke' : smoke,
                            'outside_temp' : outside_temp,
                            'status' : status,}
            else:
                status = UTC.localize(datetime.now() - timedelta(minutes=5)) < last_date
                context = {'success' : False,
                            'status' : status}
            return JsonResponse(context)
        return render(request, 'mqtt/htc.html')

    # @csrf_protect
    def post(self, request):
        last_date = max(
                Values.objects.filter(topic__name='/outside/temp').last().date_pub,
                Values.objects.filter(topic__name='/basement/kotel/water').last().date_pub,
                Values.objects.filter(topic__name='/basement/kotel/smoke').last().date_pub,
        )

        if str(request.POST.get('time')) < datetime.strftime(last_date, "%b %d, %H:%M:%S"):

            temps = [last_date.strftime("%b %d, %H:%M:%S"),
                     Values.objects.filter(topic__name='/basement/kotel/water').values('value').last()['value'],
                     Values.objects.filter(topic__name='/basement/kotel/smoke').values('value').last()['value'],
                     Values.objects.filter(topic__name='/outside/temp').values('value').last()['value'],
                    ]
            status = UTC.localize(datetime.now() - timedelta(minutes=5)) < Values.objects.all().values('date_pub').last()['date_pub']

            context = {
                        'success':True,
                        'temps':temps,
                        'status' : status,}
            return JsonResponse(context)
        else:
            status = UTC.localize(datetime.now() - timedelta(minutes=5)) < Values.objects.all().values('date_pub').last()['date_pub']
            context = {'success' : False,
                        'status' : status}
            return JsonResponse(context)
