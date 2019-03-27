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

class ImageSeries(models.Model):
    dicom_archive = models.FileField(upload_to="dicom/")
    voxel_file = models.FileField(upload_to="voxels/")
    patient_id = models.CharField(max_length=64, null=True)
    study_uid = models.CharField(max_length=64)
    series_uid = models.CharField(max_length=64)

    AccessionNumber = models.CharField(max_length=128)
    AcquisitionDate = models.CharField(max_length=128)
    AcquisitionDateTime = models.CharField(max_length=128)
    AcquisitionTime = models.CharField(max_length=128)
    BodyPartExamined = models.CharField(max_length=128)
    ContentDate = models.CharField(max_length=128)
    ContentTime = models.CharField(max_length=128)
    ConvolutionKernel = models.CharField(max_length=128)
    DerivationDescription = models.CharField(max_length=128)
    DeviceSerialNumber = models.CharField(max_length=128)
    ExposureModulationType = models.CharField(max_length=128)
    FilterType = models.CharField(max_length=128)
    InstitutionAddress = models.CharField(max_length=128)
    InstitutionName = models.CharField(max_length=128)
    InstitutionalDepartmentName = models.CharField(max_length=128)
    IssuerOfPatientID = models.CharField(max_length=128)
    Manufacturer = models.CharField(max_length=128)
    ManufacturerModelName = models.CharField(max_length=128)
    Modality = models.CharField(max_length=128)
    PatientAge = models.CharField(max_length=128)
    PatientBirthDate = models.CharField(max_length=128)
    PatientID = models.CharField(max_length=128)
    PatientPosition = models.CharField(max_length=128)
    PatientSex = models.CharField(max_length=128)
    PerformedProcedureStepID = models.CharField(max_length=128)
    PerformedProcedureStepStartDate = models.CharField(max_length=128)
    PerformedProcedureStepStartTime = models.CharField(max_length=128)
    PhotometricInterpretation = models.CharField(max_length=128)
    PositionReferenceIndicator = models.CharField(max_length=128)
    ProtocolName = models.CharField(max_length=128)
    RetrieveAETitle = models.CharField(max_length=128)
    RotationDirection = models.CharField(max_length=128)
    ScanOptions = models.CharField(max_length=128)
    ScheduledProcedureStepEndDate = models.CharField(max_length=128)
    ScheduledProcedureStepEndTime = models.CharField(max_length=128)
    ScheduledProcedureStepStartDate = models.CharField(max_length=128)
    ScheduledProcedureStepStartTime = models.CharField(max_length=128)
    SeriesDate = models.CharField(max_length=128)
    SeriesDescription = models.CharField(max_length=128)
    SeriesTime = models.CharField(max_length=128)
    SoftwareVersions = models.CharField(max_length=128)
    SpecificCharacterSet = models.CharField(max_length=128)
    StackID = models.CharField(max_length=128)
    StationAETitle = models.CharField(max_length=128)
    StationName = models.CharField(max_length=128)
    StudyDate = models.CharField(max_length=128)
    StudyID = models.CharField(max_length=128)
    StudyStatusID = models.CharField(max_length=128)
    StudyTime = models.CharField(max_length=128)

    BitsAllocated = models.IntegerField(default=0)
    BitsStored = models.IntegerField(default=0)
    Columns = models.IntegerField(default=0)
    HighBit = models.IntegerField(default=0)
    InStackPositionNumber = models.IntegerField(default=0)
    PixelRepresentation = models.IntegerField(default=0)
    Rows = models.IntegerField(default=0)
    SamplesPerPixel = models.IntegerField(default=0)
    TemporalPositionIndex = models.IntegerField(default=0)

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
        print("Debug: First layout:", dicom_datasets[0].pixel_array)
        voxels, _ = combine_slices(dicom_datasets)
        content_file = ContentFile(b'')  # empty zero byte file
        np.save(content_file, voxels)
        self.voxel_file.save(name='voxels', content=content_file, save=False)
        self._export_pngs(voxels)
        
        self.patient_id = dicom_datasets[0].PatientID
        self.study_uid = dicom_datasets[0].StudyInstanceUID
        self.series_uid = dicom_datasets[0].SeriesInstanceUID

        for att in dir(dicom_datasets[0]):
            try:
                setattr( self, att, getattr(dicom_datasets[0], att) )
                print("DEBUG IN ATTR: OK")
            except:
                print("DEBUG IN ATTR: Error")

        super(ImageSeries, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        try:
           # Delete the images folder as well
            shutil.rmtree(self.images_path)
        except:
            pass
        super(ImageSeries, self).delete(*args, **kwargs)
        
    def _export_pngs(self, voxels):
        path = self.images_path
        if not os.path.exists(path):
            os.makedirs(path)
        
        export_to_png(path, voxels)
        
    class Meta:
        verbose_name_plural = 'Image Series'
