from tifffile import TiffWriter
from PIL import Image
import numpy as np   
import sys


def tiff_to_bigtiff(tiff32_name, header_size = 8, page_size = 655654, page_resolution = (640,512), page_mode = 'I;16'):
    """ 
    Convert 32 bit multipage tiff file to 64 bit multipage big tiff file.
    This is not a general tool! It was made to convert tiff files from a specific source. See assumptions.  
    
    Args:
        tiff32_name (str):          The name of the tiff file to be converted if in this directory, or the path to the file.
        header_size (int):          The header size in bytes of the tiff file to be converted.
        page_size (int):            The constant size in bytes of each page in the tiff file to be converted.
        page_resolution (tuple):    The constant resolution of each page in the tiff file to be converted.
        page_mode (str):            The color mode of each page in the tiff file to be converted (default is 16 bit grayscale).

    Assumptions:
        1. Image data in the tiff file to be converted is uncompressed and of constant resolution because there must be a 
            constant number of bytes between each page.
        2. Tiff file is of .tif or .tiff file extension.
        3. Tiff image data is 16 bit grayscale. This script has not been tested with RGB images so performance on RGB images is unknown.
        4. All arguments are given properly and in the correct order. Some prior analysis of the tiff file may be necessary.
    """

    if tiff32_name[-4:] == '.tif':
        extension = '.tif'
    elif tiff32_name[-5:] == '.tiff':
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
            img_data = tiff32.read(page_size)
            img = Image.frombytes(mode=page_mode, size=page_resolution, data=img_data, decoder_name='raw')
            tiff64.save(np.asarray(img))

            i += 1
            if i % 200 == 0:
                sys.stdout.write(f'\rConverting {file_to_convert} to 64 bit... {tiff32.tell()/end_of_file*100 :.2f}%')
                sys.stdout.flush()

        print('\nFinished conversion\n')


if __name__ == "__main__":
    file_to_convert = sys.argv[1]
    tiff_to_bigtiff(file_to_convert)
