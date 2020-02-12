from tifffile import TiffFile
from PIL import Image
import numpy as np
import sys

def validate_bigtiff(tiff64_name, tiff32_name, tiff32_header_size = 8, tiff32_image_size = 655654):
    """ Validates that all frames in a 64 bit TIFF file are the same as the frames in its corresponding 32 bit TIFF file """
    tiff64 = TiffFile(tiff64_name)
    
    with open(tiff32_name, 'rb') as tiff32:
        tiff32.seek(0, 2)
        end_of_tiff32 = tiff32.tell()

        # Skip header
        tiff32.seek(tiff32_header_size)

        for i, page in enumerate(tiff64.pages):
            img_data = tiff32.read(tiff32_image_size)
            img = Image.frombytes(mode='I;16', size=(640,512), data=img_data, decoder_name='raw')

            # Validate frame
            if not (np.asarray(img) == page.asarray()).all():
                raise Exception('64 bit tff != 32 bit tiff')

            if i % 200 == 0:
                sys.stdout.write(f'\rValidating {tiff64_name} for equivalency to {tiff32_name}... {i/len(tiff64.pages)*100 :.2f}%')
                sys.stdout.flush()
        
        print('\nFinished validation, tiff files have equivalent data')


if __name__ == "__main__":
    converted_file, original_file = sys.argv[1:3]
    validate_bigtiff(converted_file, original_file)
