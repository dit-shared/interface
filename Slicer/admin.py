from django.contrib import admin

from .models import ImageSeries, SeriesInfo

@admin.register(SeriesInfo)
class SeriesInfoAdmin(admin.ModelAdmin):
    readonly_fields = ("doctorComment", "doctorCommentDate", "seriesID")

@admin.register(ImageSeries)
class ImageSeriesAdmin(admin.ModelAdmin):
    readonly_fields = ('voxel_file', 'patient_id', 'study_uid', 'series_uid', 'AccessionNumber',
        'AcquisitionDate', 'FilterType', 'PatientAge', 'PatientBirthDate', 'PatientID',
        'PatientPosition', 'PatientSex', 'ScanOptions',
        'SeriesDate', 'SeriesDescription', 'SeriesTime', 'SoftwareVersions',
        'StationName', 'StudyDate', 'StudyID', 'StudyStatusID', 'StudyTime')
