# Convert 32 bit to 64 bit TIFF

Converts a 32 bit multipage tiff file to a 64 bit multipage big tiff file.

This is not a general tool! It was made to convert 16 bit grayscale tiff files from a specific source. 
Specifically, tiff files from a FLIR thermal imaging camera that are larger than 4.3 GB.
Performance on tiff files from other sources is unknown. 

**Usage:** `python3 tiff_to_bigtiff.py <filename.tiff>`

## Installation

1. Clone this repository
2. Set up a python virtual environment in the cloned directory
3. Install required packages using `pip install -r requirements.txt`
