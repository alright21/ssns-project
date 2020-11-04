from django.http import HttpResponse
from measures.models import Measure
from django.shortcuts import render
from django.db.models import Max
from django.http import JsonResponse


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def dashboard(request):
    return render(request, 'dashboard.html')

def shelves_chart(request):
    labels = []
    range_data = []
    light_data = []

    # queryset = Measure.objects.values('node_id').annotate(range=Sum('range')).order_by('node_id')
    # queryset = Measure.objects.values('node_id','range').annotate(latest=Max('timestamp'))
    queryset = Measure.objects.raw('select s1.* from measures_measure as s1 inner join (select node_id, max(timestamp) as mts FROM measures_measure GROUP BY node_id) s2 ON s2.node_id=s1.node_id and s1.timestamp=s2.mts ORDER BY node_id ASC')
    for i in queryset:
        print(i.range)

    for entry in queryset:
        labels.append(entry.node_id)
        range = 50
        if entry.range > 50:
            if entry.light>0:
                range = 0
            else:
                range=10
        elif entry.range < 1:
            range = 100
        else:
            range = translate(entry.range, 0, 100, -100, 0)
            range = -range
        
        range_data.append(range)
        light = entry.light
        
        if light == 0:
            light_data.append(0)
        else:
            light_data.append(50)

        

    return JsonResponse(data={
        'labels': labels,
        'range_data': range_data,
        'light_data': light_data
    })
