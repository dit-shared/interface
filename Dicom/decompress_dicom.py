import gdcm

def decompress(compressed_file):
	change = gdcm.ImageChangeTransferSyntax()
	change.SetTransferSyntax( gdcm.TransferSyntax( gdcm.TransferSyntax.ImplicitVRLittleEndian ) )
	change.SetInput( compressed_file )

	writer = gdcm.ImageWriter()
	writer.SetFileName( file2 )
	writer.SetFile( read.GetFile() )
	writer.SetImage( change.GetOutput() )

    # TODO!!!