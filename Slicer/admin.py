from django.contrib import admin

from .models import ImageSeries

# admin.site.register(ImageSeries)

@admin.register(ImageSeries)
class ImageSeriesAdmin(admin.ModelAdmin):
    readonly_fields = ('voxel_file', 'patient_id', 'study_uid', 'series_uid', 'BitsAllocated',
        'BitsStored', 'Columns', 'HighBit', 'InStackPositionNumber', 'PixelRepresentation', 'Rows',
        'SamplesPerPixel', 'TemporalPositionIndex', 'AccessionNumber', 'AcquisitionDate', 'AcquisitionDateTime',
        'AcquisitionTime', 'BodyPartExamined', 'ContentDate', 'ContentTime', 'ConvolutionKernel',
        'DerivationDescription', 'DeviceSerialNumber', 'ExposureModulationType', 'FilterType',
        'InstitutionAddress', 'InstitutionName', 'InstitutionalDepartmentName', 'IssuerOfPatientID',
        'Manufacturer', 'ManufacturerModelName', 'Modality', 'PatientAge', 'PatientBirthDate', 'PatientID',
        'PatientPosition', 'PatientSex', 'PerformedProcedureStepID', 'PerformedProcedureStepStartDate',
        'PerformedProcedureStepStartTime', 'PhotometricInterpretation', 'PositionReferenceIndicator',
        'ProtocolName', 'RetrieveAETitle', 'RotationDirection', 'ScanOptions', 'ScheduledProcedureStepEndDate',
        'ScheduledProcedureStepEndTime', 'ScheduledProcedureStepStartDate', 'ScheduledProcedureStepStartTime',
        'SeriesDate', 'SeriesDescription', 'SeriesTime', 'SoftwareVersions', 'SpecificCharacterSet', 'StackID',
        'StationAETitle', 'StationName', 'StudyDate', 'StudyID', 'StudyStatusID', 'StudyTime')
