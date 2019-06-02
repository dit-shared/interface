from django.conf import settings
from django.db import models
from Slicer.dicom_import import dicom_datasets_from_zip
from Slicer.dicom_export import export_to_png

#from django.conf.urls.static import static
#from django.core.files.base import ContentFile
#import numpy as np

import os, shutil, zipfile, datetime, hashlib

class SeriesInfo(models.Model):
    doctorComment = models.CharField(max_length=256, default="")
    doctorCommentDate = models.DateTimeField(default=datetime.date.today, null=True, blank=True)
    seriesID = models.IntegerField()
    slicesCnt = models.IntegerField(null=True, blank=True)

    AccessionNumber = models.CharField(max_length=128)
    AcquisitionDate = models.CharField(max_length=128)
    FilterType = models.CharField(max_length=128)
    PatientID = models.CharField(max_length=128)
    PatientAge = models.CharField(max_length=128)
    PatientBirthDate = models.CharField(max_length=128)
    PatientPosition = models.CharField(max_length=128)
    StudyID = models.CharField(max_length=128)
    PatientSex = models.CharField(max_length=128)
    ScanOptions = models.CharField(max_length=128)
    SeriesDate = models.CharField(max_length=128)
    SeriesDescription = models.CharField(max_length=128)
    SeriesTime = models.CharField(max_length=128)
    SoftwareVersions = models.CharField(max_length=128)
    StationName = models.CharField(max_length=128)
    StudyDate = models.CharField(max_length=128)
    StudyStatusID = models.CharField(max_length=128)
    SeriesInstanceUID = models.CharField(max_length=128)
    StudyTime = models.CharField(max_length=128)
    Manufacturer = models.CharField(max_length=128)

    previewSlice = models.CharField(max_length=32, default="0_gray.png")
    slices_dir = models.CharField(max_length=128)

class ImageSeries(models.Model):
    dicom_archive = models.FileField(upload_to="dicom/")
    patient_id = models.CharField(max_length=64, null=True)
    study_uid = models.CharField(max_length=64)
    series_uid = models.CharField(max_length=64)

    # @property
    # def media_path(self):
    #     with self.voxel_file as f:
    #         path = os.path.basename(f.name)
    #     return path
    
    @property
    def images_path(self):
        return settings.MEDIA_ROOT + "/images/" + self.slices_dir
    
    def save(self, *args, **kwargs):
        with zipfile.ZipFile(self.dicom_archive, 'r') as f:
            dicom_datasets = dicom_datasets_from_zip(f)
        dicom_datasets.sort(key=lambda x: x.ImagePositionPatient[2])

        self.slices_dir = hashlib.sha256(self.study_uid.encode()).hexdigest()
        self.patient_id = dicom_datasets[0].PatientID
        self.study_uid = dicom_datasets[0].StudyInstanceUID
        self.series_uid = dicom_datasets[0].SeriesInstanceUID

        self._export_pngs(dicom_datasets)

        super(ImageSeries, self).save(*args, **kwargs)

        si = SeriesInfo.objects.create(seriesID=self.id)
        si.slices_dir = self.slices_dir
        si.slicesCnt = len(dicom_datasets)

        for att in dir(dicom_datasets[0]):
            try:
                setattr( si, att, getattr(dicom_datasets[0], att) )
            except:
                pass
        si.save()

        
    def delete(self, *args, **kwargs):
        try:
           # Delete the images folder as well
            shutil.rmtree(self.images_path)
        except:
            pass
        super(ImageSeries, self).delete(*args, **kwargs)
        
    def _export_pngs(self, dic_ds):
        path = self.images_path
        if not os.path.exists(path):
            os.makedirs(path)
        export_to_png(path, dic_ds)
        
    class Meta:
        verbose_name_plural = 'Image Series'
