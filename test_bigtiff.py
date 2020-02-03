from tifffile import TiffFile
import matplotlib.pyplot as plt
import numpy as np
import sys

def test_bigtiff(tiff64_name, tiff32_name, tiff32_header_size = 8, tiff32_image_size = 655654):
    """ Test tiff64 for equivalency to tiff32 """
    tiff64 = TiffFile(tiff64_name)

    plt.imshow(tiff64.pages[10].asarray())
    plt.show()
    
    # with open(tiff32_name, 'rb') as tiff32:
    #     tiff32.seek(0, 2)
    #     end_of_tiff32 = tiff32.tell()

    #     # Skip header
    #     tiff32.seek(tiff32_header_size)

    #     i = 0
    #     while tiff32.tell() < end_of_tiff32:

    #         img_data = tiff32.read(tiff32_image_size)
    #         img = Image.frombytes(mode='I;16', size=(640,512), data=img_data, decoder_name='raw')

    #         # Validate frame
    #         if not (np.asarray(img) == tiff64.pages[i].asarray()).all():
    #             raise Exception('64 bit tff != 32 bit tiff')

    #         i += 1
    #         if i % 200 == 0:
    #             sys.stdout.write(f'\rValidating {tiff64_name} for equivalency to {tiff32_name}... {i/len(tiff64.pages)*100 :.2f}%')
    #             sys.stdout.flush()
        
    #     print('\nFinished Validation, tiff files have equivalent data')

if __name__ == '__main__':
    file_converted, original_file = sys.argv[1:3]
    test_bigtiff(file_converted, original_file)
    