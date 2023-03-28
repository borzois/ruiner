import os
import re
import shutil

import PIL.Image
from PIL import Image

import argparse
 
 
# first iteration = 100%
# last iteration = dip_percentage
def interpolated_dip(iteration, total_iterations, dip_percentage):
    p = iteration / total_iterations
    return p * dip_percentage + (1 - p) * 100


def prepare_directory():
    if not os.path.exists("tmp/"):
        os.makedirs("tmp/")


def remove_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

class Ruiner:
    def __init__(self, args):
        self._args = args
        prepare_directory()
        self._images = []
        self._image_path = os.path.abspath(self._args.filename)
        self._images.append(self.prepare_image())
        self._image_size = self._images[0].size
        self._filters = {
            'NEAREST': PIL.Image.NEAREST,
            'LANCZOS': PIL.Image.LANCZOS,
            'BILINEAR': PIL.Image.BILINEAR,
            'BICUBIC': PIL.Image.BICUBIC,
            'BOX': PIL.Image.BOX,
            'HAMMING': PIL.Image.HAMMING,
        }

    def prepare_image(self):
        with Image.open(self._image_path) as im:
            print("loaded " + self._image_path)
            im = im.convert("RGB")
            im.save("tmp/compressed0.jpg", "JPEG")
            return im

    def convert_to_RGB(self):
        with Image.open(self._image_path) as im:
            im = im.convert("RGB")
            print("bad color mode, converting to RGB!")
            return im

    def export_image(self):
        image_filename = os.path.splitext(self._image_path)[0] + "_" + self._args.procedure + "_RUINED.jpg"
        self._images[-1].save(image_filename, "JPEG")
        print("image exported at " + image_filename)

    def export_gif(self):
        print("generating gif")
        gif_filename = os.path.splitext(self._image_path)[0] + "_" + self._args.procedure + "_DECAY.gif"
        gif_speed = self._args.speed
        self._images[0].save(gif_filename,
                             save_all=True,
                             append_images=[self._images[i] for i in range(1, len(self._images)) if i % gif_speed == 0],
                             optimize=True)
        print("gif exported at " + gif_filename)

    def cleanup(self):
        print("cleaning up")
        remove_directory("tmp/")
        print("done")

    def ruin(self):
        proc = re.split('\W+', self._args.procedure)
        iterations = self._args.iterations
        for i in range(0, iterations):
            infile = "tmp/compressed" + str(i) + ".jpg"
            outfile = "tmp/compressed" + str(i + 1) + ".jpg"
            with Image.open(infile) as im:
                current_dip = interpolated_dip(i, iterations, self._args.resize)
                print("current image: " + outfile + "; current resize: " + str(int(current_dip)) + "%; ", end='')

                for operation in proc:
                    if operation == 'cYCbCr':
                        print("convert to YCbCr; ", end='')
                        im = im.convert("YCbCr")
                    elif operation == 'cRGB':
                        print("convert to RGB; ", end='')
                        im = im.convert("RGB")
                    elif operation.startswith('r'):
                        current_filter = self._filters[operation[1:]]
                        print("shrink " + str(current_filter) + "; ", end='')
                        im = im.resize(
                            (int(self._image_size[0] * current_dip / 100),
                             int(self._image_size[1] * current_dip / 100)),
                            resample=current_filter)
                    elif operation.startswith('R'):
                        current_filter = self._filters[operation[1:]]
                        print("enlarge " + str(current_filter) + "; ", end='')
                        im = im.resize(self._image_size, resample=current_filter)
                    elif operation.startswith('t'):
                        angle = int(operation[1:])
                        print("tilt " + str(angle) + "; ", end='')
                        im = im.rotate(angle, expand=True)

                self._images.append(im)
                im.save(outfile, "JPEG")
                print('')

        if im.mode != "RGBA":
            self.convert_to_RGB()
        self.export_image() 
        if self._args.gif:
            self.export_gif()
        if not self._args.keep_temp:
            self.cleanup()
        return self._images[-1]


def get_args():
    parser = argparse.ArgumentParser(description="image destruction toolkit")
    parser.add_argument("-i", "--iterations", type=int, help="Number of times to compress")
    parser.add_argument("-r", "--resize", type=int, help="Percentage to resize to")
    parser.add_argument("-s", "--speed", type=int, default=1, help="GIF speed multiplier (only use every s-th frame)")
    parser.add_argument("--gif", action=argparse.BooleanOptionalAction, default=False, help="Generates a gif")
    parser.add_argument("--keep-temp", action=argparse.BooleanOptionalAction, default=False, help="Keeps temp files")
    parser.add_argument("-p", "--procedure", type=str, help="Procedure (see readme)")
    parser.add_argument("filename", type=str, help="Input Filename")

    return parser.parse_args()


def main():
    args = get_args()
    ruiner = Ruiner(args)
    result = ruiner.ruin()


if __name__ == '__main__':
    main()
    