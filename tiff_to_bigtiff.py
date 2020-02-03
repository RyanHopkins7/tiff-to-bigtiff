from tifffile import TiffWriter
from PIL import Image
import numpy as np   
import sys


def tiff_to_bigtiff(file_to_convert, header_size = 8, image_size = 655654):
    """ Convert file_to_convert to a 64 bit BigTiff file """

    with open(file_to_convert, 'rb') as tiff32, TiffWriter(file_to_convert[:-5] + 'x64.tiff', bigtiff=True) as tiff64:
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


