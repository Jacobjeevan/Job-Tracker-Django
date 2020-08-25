from django.shortcuts import render, get_list_or_404
from .models import Job, Location
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
import random
import requests
import os
import jsonpickle
from users.models import User


def home(request):
    currentuser = getUserorTestUser(request.user)
    context = getData(currentuser)
    return render(request, 'mainpage/home.html', context=context)


def getData(currentuser):
    joblist = Job.objects.filter(author=currentuser).all()
    features = []
    for i in joblist:
        loc = Location.objects.filter(city=i.city, state=i.state).first()
        features.append({'type': 'Feature', 'properties': {'description': f"{i.title} at {i.employer}"},
                         'geometry': {'type': 'Point', 'coordinates': [loc.longitude+0.001*random.random(), loc.latitude+0.001*random.random()]}})
    data = {'type': 'geojson', 'data': {
        'type': 'FeatureCollection', 'features': features}}
    context = {'data': jsonpickle.encode(data), 'MAPBOX_KEY': os.environ.get(
        'MAPBOX_KEY'), 'map_center': [-98.57, 39.82]}
    return context


def getUserorTestUser(currentuser):
    if (currentuser is None or currentuser.is_anonymous):
        return User.objects.filter(username='testUser').first()
    return currentuser


class JobListView(ListView):
    model = Job
    template_name = 'mainpage/job-home.html'
    context_object_name = 'jobs'
    paginate_by = 6

    def get_queryset(self):
        currentuser = getUserorTestUser(self.request.user)
        return Job.objects.filter(author=currentuser)


class LocationListView(ListView):
    model = Job
    template_name = 'mainpage/location_jobs.html'
    context_object_name = 'jobs'
    paginate_by = 6

    def get_queryset(self):
        city = self.kwargs.get('city')
        state = self.kwargs.get('state')
        currentuser = getUserorTestUser(self.request.user)
        return Job.objects.filter(city=city, state=state, author=currentuser)


class EmployerListView(ListView):
    model = Job
    template_name = 'mainpage/employer_jobs.html'
    context_object_name = 'jobs'
    paginate_by = 6

    def get_queryset(self):
        employer = self.kwargs.get('employer')
        currentuser = getUserorTestUser(self.request.user)
        return Job.objects.filter(employer=employer, author=currentuser)


class StatusListView(ListView):
    model = Job
    template_name = 'mainpage/status_jobs.html'
    context_object_name = 'jobs'
    paginate_by = 6

    def get_queryset(self):
        status = self.kwargs.get('status')
        currentuser = getUserorTestUser(self.request.user)
        return Job.objects.filter(status=status, author=currentuser)


class JobDetailView(DetailView):
    model = Job

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['MAPBOX_KEY'] = os.environ.get('MAPBOX_KEY')
        context['data'], context['map_center'] = self.getData()
        return self.render_to_response(context)

    def getData(self):
        latitude = self.object.location.latitude
        longitude = self.object.location.longitude
        features = [{'type': 'Feature', 'properties': {'description': f"{self.object.title} at {self.object.employer}"},
                     'geometry': {'type': 'Point', 'coordinates':
                                  [longitude+0.001*random.random(),
                                   latitude+0.001*random.random()]}}]
        data = {'type': 'geojson', 'data': {
            'type': 'FeatureCollection', 'features': features}}
        map_center = [longitude, latitude]
        data = jsonpickle.encode(data)
        return data, map_center


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    fields = ['title', 'employer', 'apply_date',
              'description', 'status', 'city', 'state']

    def form_valid(self, form):
        form.instance.author = self.request.user
        city = form.instance.city
        state = form.instance.state
        form.instance.location = LocationCreationUpdation(
            city, state).getLocation()
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    fields = ['title', 'employer', 'apply_date',
              'description', 'status', 'city', 'state']

    def form_valid(self, form):
        form.instance.author = self.request.user
        city = form.instance.city
        state = form.instance.state
        form.instance.location = LocationCreationUpdation(
            city, state).getLocation()
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class LocationCreationUpdation:

    def __init__(self, city, state):
        self.city = city
        self.state = state

    def getLocation(self):
        NewLocation = Location.objects.filter(city=self.city, state=self.state)
        location = list(NewLocation)
        if not location:
            NewLocation = self.createNewLocation()
        else:
            NewLocation = NewLocation.first()
        return NewLocation

    def createNewLocation(self):
        r = self.getCoordinates()
        if r.status_code == 200:
            response = r.json()
            latitude = response['data'][0]['latitude']
            longitude = response['data'][0]['longitude']
            NewLocation = Location(
                city=self.city, state=self.state, latitude=latitude, longitude=longitude)
            NewLocation.save()
            return NewLocation

    def getCoordinates(self):
        payload = {'access_key': os.environ.get(
            'MAP_API_KEY'), 'query': f"{self.city},{self.state}", 'limit': 1}
        r = requests.get(os.environ.get('MAP_URL'), params=payload)
        return r


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
