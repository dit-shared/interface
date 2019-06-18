from Frontend import settings
import time, os, zipfile, random, string, tempfile, gdcm
from matplotlib import pyplot as plt
import pydicom as dicom

COLOR_MAPS = ("COLORMAP_BONE", "COLORMAP_JET", "COLORMAP_HOT")
cmaps = {"bone": plt.cm.bone, "gray": plt.cm.gray}

def SliceResearch(filename, status, progress):
	status.value = 1
	zipFilePath = "{}/zips/{}".format(settings.MEDIA_ROOT, filename)	

	datasets = list()
	with zipfile.ZipFile(zipFilePath) as researchZip:
		for entry in researchZip.namelist():
			if entry.endswith('/'):
				continue  # skip directories
			entryPseudoFile = researchZip.open(entry)

			dicomTempFile = tempfile.NamedTemporaryFile()
			dicomTempFile.write(entryPseudoFile.read())
			dicomTempFile.flush()
			dicomTempFile.seek(0)

			try:
				dataset = dicom.read_file(dicomTempFile)
				dataset.pixel_array
				datasets.append(dataset)
			except dicom.errors.InvalidDicomError as e:
				print(e)
				pass

	datasetsCnt = len(datasets)
	if datasetsCnt == 0:
		status.value = 124
		return

	status.value = 2

	imageDirPath = "{}/images/{}".format(settings.MEDIA_ROOT, "test")

	if not os.path.exists(imageDirPath):
		os.makedirs(imageDirPath)

	for n, ds in enumerate(datasets):
		image = str(n) + "_{}.png"
		for cmName, cm in cmaps.items():
			fig = plt.figure(frameon=False, dpi=300)
			ax = plt.Axes(fig, [0., 0., 1., 1.])
			ax.set_axis_off()
			fig.add_axes(ax)
			# Axes.imshow(ds.pixel_array, cmap=cm)     
			plt.savefig(os.path.join(imageDirPath, image.format(cmName)))
			plt.close()
		progress.value = (n * 100) / datasetsCnt