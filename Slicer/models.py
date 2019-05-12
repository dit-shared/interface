import numpy as np

from django.conf import settings
from django.conf.urls.static import static
from django.core.files.base import ContentFile
from django.db import models

import os
import shutil

from Slicer.dicom_import import dicom_datasets_from_zip, combine_slices
from Slicer.dicom_export import export_to_png

import zipfile

class SeriesInfo(models.Model):
    doctorComment = models.CharField(max_length=256, default="")
    doctorCommentDate = models.DateTimeField(auto_now_add=True, blank=True)
    seriesID = models.IntegerField()

class ImageSeries(models.Model):
    dicom_archive = models.FileField(upload_to="dicom/")
    voxel_file = models.FileField(upload_to="voxels/")
    patient_id = models.CharField(max_length=64, null=True)
    study_uid = models.CharField(max_length=64)
    series_uid = models.CharField(max_length=64)

    AccessionNumber = models.CharField(max_length=128)
    AcquisitionDate = models.CharField(max_length=128)
    FilterType = models.CharField(max_length=128)
    PatientAge = models.CharField(max_length=128)
    PatientBirthDate = models.CharField(max_length=128)
    PatientID = models.CharField(max_length=128)
    PatientPosition = models.CharField(max_length=128)
    PatientSex = models.CharField(max_length=128)
    ScanOptions = models.CharField(max_length=128)
    SeriesDate = models.CharField(max_length=128)
    SeriesDescription = models.CharField(max_length=128)
    SeriesTime = models.CharField(max_length=128)
    SoftwareVersions = models.CharField(max_length=128)
    StationName = models.CharField(max_length=128)
    StudyDate = models.CharField(max_length=128)
    StudyID = models.CharField(max_length=128)
    StudyStatusID = models.CharField(max_length=128)
    StudyTime = models.CharField(max_length=128)

    @property
    def voxels(self):
        with self.voxel_file as f:
            voxel_array = np.load(f)
        return voxel_array

    @property
    def media_path(self):
        with self.voxel_file as f:
            path = os.path.basename(f.name)
        return path
    
    @property
    def images_path(self):
        with self.voxel_file as f:
            path = settings.MEDIA_ROOT + "/images/" + os.path.basename(f.name)
        return path
    
    def save(self, *args, **kwargs):
        with zipfile.ZipFile(self.dicom_archive, 'r') as f:
            dicom_datasets = dicom_datasets_from_zip(f)
        dicom_datasets.sort(key=lambda x: x.ImagePositionPatient[2])
        print("Debug: First layout:", dicom_datasets[0].pixel_array)
        voxels, _ = combine_slices(dicom_datasets)
        content_file = ContentFile(b'')  # empty zero byte file
        np.save(content_file, voxels)
        self.voxel_file.save(name='voxels', content=content_file, save=False)
        self._export_pngs(dicom_datasets)
        
        self.patient_id = dicom_datasets[0].PatientID
        self.study_uid = dicom_datasets[0].StudyInstanceUID
        self.series_uid = dicom_datasets[0].SeriesInstanceUID

        for att in dir(dicom_datasets[0]):
            try:
                setattr( self, att, getattr(dicom_datasets[0], att) )
            except:
                pass
        super(ImageSeries, self).save(*args, **kwargs)
        SeriesInfo.objects.create(seriesID=self.id)
        
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
