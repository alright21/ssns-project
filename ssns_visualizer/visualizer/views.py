from django.http import HttpResponse
from measures.models import Measure
from django.shortcuts import render
from django.db.models import Max
from django.http import JsonResponse
# Import Datetime
from datetime import datetime


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def map_range(input):

    distance = 50
    if input > 50:
        if input > 0:
            distance = 0
        else:
            distance = 10
    elif input < 1:
        distance = 50
    else:
        distance = translate(input, 0, 50, -100, 0)
        distance = -distance
    return distance


def dashboard(request):

    istant_labels = []
    range_data = []
    light_data = []

    queryset = Measure.objects.raw(
        'select s1.* from measures_measure as s1 inner join (select node_id, max(timestamp) as mts FROM measures_measure GROUP BY node_id) s2 ON s2.node_id=s1.node_id and s1.timestamp=s2.mts ORDER BY node_id ASC')

    for entry in queryset:
        istant_labels.append(entry.node_id)
        
        range_data.append(map_range(entry.range))
        light = entry.light

        if light == 0:
            light_data.append(0)
        else:
            light_data.append(50)

    history = []


    for i in range(1, 5):

        print(i)
        queryset = list(Measure.objects.filter(node_id=i))[-10:]
        labels = []
        data = []

        for entry in queryset:

            formatedDate = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            labels.append(formatedDate)
            data.append(map_range(entry.range))

        history.append({
            'labels': labels,
            'data': data
            })

    print(history)

    return render(request, 'dashboard.html', {
        'istant': {
            'labels': istant_labels,
            'range_data': range_data,
            'light_data': light_data
        },
        'history': history

    })
