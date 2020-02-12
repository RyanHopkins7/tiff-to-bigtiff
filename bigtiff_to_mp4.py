from tifffile import TiffWriter, imread, TiffFile
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from random import choice


def bigtiff_to_mp4(tiff64_name):
    """ Converts a 64 bit TIFF file to an mp4 file """

    tiff64 = TiffFile(tiff64_name)

    display_min = 23500
    display_max = 24700

    videodims = (640,512)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')    

    # tiff64_name[:-5] -> tiff64_name[:-4] if .tif instead of .tiff
    video = cv2.VideoWriter(tiff64_name[:-5]+'.mp4' , fourcc, 30, videodims, False)

    for i, page in enumerate(tiff64.pages):
        image = page.asarray()
        image.clip(display_min, display_max, out=image)
        image -= display_min
        np.floor_divide(image, (display_max - display_min + 1) / 256, out=image, casting='unsafe')

        video.write(image.astype('uint8'))

        if i % 200 == 0:
            sys.stdout.write(f'\rConverting {tiff64_name} to {tiff64_name[:-5]}.mp4... {i/len(tiff64.pages)*100 :.2f}%')
            sys.stdout.flush()
        
    video.release()
    print('\nFinished conversion')


if __name__ == "__main__":
    file_to_convert = sys.argv[1]
    bigtiff_to_mp4(file_to_convert)

