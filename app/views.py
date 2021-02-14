import urllib
from urllib.parse import urlencode
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
import csv


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):

    current_page = int(request.GET.get('page', 1))

    with open(settings.BUS_STATION_CSV) as file:
        reader = csv.DictReader(file)
        bus_stations_dict_list = list()

        for row in reader:
            name = row['Name']
            street = row['Street']
            district = row['District']
            bus_stations_dict_list.append({'Name': name, 'Street': street, 'District': district})
            paginator = Paginator(bus_stations_dict_list, 10)
            page = paginator.get_page(current_page)
            msg = page.object_list

        if page.has_next():
            next_page_url_param = urllib.parse.urlencode({'page': page.next_page_number()})
            next_page_url = reverse(bus_stations) + '?' + next_page_url_param
        else:
            next_page_url = None

        if page.has_previous():
            prev_page_url_param = urllib.parse.urlencode({'page': page.previous_page_number()})
            prev_page_url = reverse(bus_stations) + '?' + prev_page_url_param
        else:
            prev_page_url = None

    return render(request, 'index.html', context={
        'bus_stations': msg,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })
