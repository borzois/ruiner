# Ruiner
#### A JPEG compression based image destruction toolkit
![](example.gif)

## Dependencies
- python >= 3.9
- Pillow
- argparse
```
pip install Pillow argparse
```

## Usage
```
ruiner.py [-h] [-i ITERATIONS] [-r RESIZE] [-s SPEED] [--gif | --no-gif] [-p PROCEDURE] filename
```

## Procedure
The program works based on a loop that is executed *ITERATIONS* times

`load previously saved image -> perform PROCEDURE -> save image`

The procedure is described using a string of keywords, delimited using spaces
#### Keywords
```
r[FILTER] - resize (usually shrink) the image using the selected filter
R[FILTER] - resize the image to its original size using the selected filter
c[MODE] - convert the image to a different colorspace
```

##### Filters
Ruiner supports all the filters built into Pillow
```
NEAREST - creates interesting artifacts depending on the resize parameter
LANCZOS
BILINEAR
BICUBIC
BOX
HAMMING
```

##### Modes
Ruiner currently supports 2 modes
```
RGB - standard colorspace
YCbCr - useful for getting the green tint
```

#### Resizing
The `-r` argument describes the resize factor on the *final* iteration, 
but the actual factor gradually decreases from 100% during the execution.

### Examples
`ruiner.py -i 400 -r 15 -p "rNEAREST cYCbCr cRGB RLANCZOS" --gif ./image.jpg`

The image is:
- loaded
- scaled down to *15%* of its original size using *nearest neighbor* filtering
- converted to *YCbCr* color space
- converted to *RGB* color space
- scaled back to its original size using *Lanczos* filtering
- saved and passed to the next iteration

This repeats *400 times*. Afterwards, the final image is saved and a *gif* is generated using the *400* iterations 