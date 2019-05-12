from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render

from .models import ImageSeries, SeriesInfo
from Account.models import User, ExtendedUser
from django.utils import timezone
import json

def buildJSONResponse(responseData):
    return HttpResponse(json.dumps(responseData), content_type="application/json")

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
        seriesInfo = SeriesInfo.objects.get(seriesID=request.GET['id'])
        voxels = series.voxels
        
        return render(request, 'Slicer/image_series_view.html', {
            'series': series,
            'voxels': voxels,
            'user': user,
            'extUser': extUser,
            'seriesInfo': seriesInfo,
        })
    return HttpResponse('Invalid request')

def changeDocComment(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']
    if not User.objects.filter(id=id):
        return HttpResponseRedirect('/')
    user = User.objects.get(id=id)
    extUser = ExtendedUser.objects.get(userID=id)

    if 'id' in request.POST and 'comment' in request.POST:
        comment = request.POST["comment"]
        seriesID = request.POST["id"]
        if comment == "":
            return buildJSONResponse({"ok": False, "msg": "Комментарий не должен быть пустым"})
        if len(comment) > 250:
            return buildJSONResponse({"ok": False, "msg": "Комментарий не должен быть длиннее 350 символов"})
        
        series = SeriesInfo.objects.get(seriesID=seriesID)
        series.doctorComment = comment
        series.doctorCommentDate = timezone.now()
        series.save()
        return buildJSONResponse({"ok": True})
    return buildJSONResponse({"ok": False, "msg": "Invalid request"})
