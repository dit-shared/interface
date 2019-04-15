from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render

from .models import ImageSeries
from Account.models import User, ExtendedUser

def image_series_view(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']
    if not User.objects.filter(id=id):
        return HttpResponseRedirect('/')
    user = User.objects.get(id=id)
    extUser = ExtendedUser.objects.get(userID=id)

    if 'id' in request.GET:
        series = ImageSeries.objects.get(id=request.GET['id'])
        voxels = series.voxels
        
        return render(request, 'Slicer/image_series_view.html', {
            'series': series,
            'voxels': voxels,
            'user': user,
            'extUser': extUser,
        })
    return HttpResponse('Invalid request')
