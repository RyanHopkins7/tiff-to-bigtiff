from tifffile import TiffWriter
from PIL import Image
import numpy as np   
import sys


def tiff_to_bigtiff(tiff32_name, header_size = 8, image_size = 655654):
    """ Convert tiff32 to a 64 bit BigTiff file """

    if tiff32_name[:-4] == '.tif':
        extension = '.tif'
    elif tiff32_name[:-5] == '.tiff'
        extension = '.tiff'
    else:
        raise ValueError('File to convert must be a .tif or .tiff file')

    with open(tiff32_name, 'rb') as tiff32, TiffWriter(tiff32_name[:-len(extension)] + 'x64.tiff', bigtiff=True) as tiff64:
        
        tiff32.seek(0, 2)
        end_of_file = tiff32.tell()

        # Skip header
        tiff32.seek(header_size)

        i = 0
        while tiff32.tell() < end_of_file:
            # Construct and validate each frame
            img_data = tiff32.read(image_size)
            img = Image.frombytes(mode='I;16', size=(640,512), data=img_data, decoder_name='raw')
            tiff64.save(np.asarray(img))

            i += 1
            if i % 200 == 0:
                sys.stdout.write(f'\rConverting {file_to_convert} to 64 bit... {tiff32.tell()/end_of_file*100 :.2f}%')
                sys.stdout.flush()

        print('\nFinished conversion\n')


if __name__ == "__main__":
    file_to_convert = sys.argv[1]
    tiff_to_bigtiff(file_to_convert)


