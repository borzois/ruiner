import time

import PIL.Image
from PIL import Image


# first iteration = 100%
# last iteration = dip_percentage
# p = 0.00.. at first, 1 at last
def interpolated_dip(iteration, total_iterations, dip_percentage):
    p = iteration/total_iterations
    return p * dip_percentage + (1-p) * 100


def jpeg_blast(iterations, dip_percentage):
    images = []
    default_infile = "default.jpg"
    default_outfile = "compressed0.jpg"
    with Image.open(default_infile) as im:
        images.append(im)
        im.save(default_outfile, "JPEG")
    for i in range(0, iterations):
        infile = "compressed" + str(i) + ".jpg"
        outfile = "compressed" + str(i+1) + ".jpg"
        with Image.open(infile) as im:
            original_size = im.size
            current_dip = interpolated_dip(i, iterations, dip_percentage)
            print("saving" + outfile + " " + str(current_dip) + "%")

            im = im.resize((int(original_size[0]*current_dip/100), int(original_size[1]*current_dip/100)))
            im = im.convert("YCbCr")
            im = im.resize(original_size)
            im = im.convert("RGB")
            images.append(im)
            im.save(outfile, "JPEG")
    return images


def jpeg_blast_alien(iterations, dip_percentage):
    images = []
    default_infile = "default.jpg"
    default_outfile = "compressed0.jpg"
    with Image.open(default_infile) as im:
        images.append(im)
        im = im.convert("RGB")
        im.save(default_outfile, "JPEG")
    for i in range(0, iterations):
        infile = "compressed" + str(i) + ".jpg"
        outfile = "compressed" + str(i+1) + ".jpg"
        with Image.open(infile) as im:
            original_size = im.size
            current_dip = interpolated_dip(i, iterations, dip_percentage)
            print("saving" + outfile + " " + str(current_dip) + "%")

            im = im.resize((int(original_size[0]*current_dip/100), int(original_size[1]*current_dip/100)),
                           resample=PIL.Image.NEAREST)
            im = im.convert("YCbCr")
            im = im.resize(original_size)
            im = im.convert("RGB")
            images.append(im)
            im.save(outfile, "JPEG")
    return images


def jpeg_blast_alien_v2(iterations, dip_percentage):
    images = []
    default_infile = "default.jpg"
    default_outfile = "compressed0.jpg"
    with Image.open(default_infile) as im:
        images.append(im)
        im.save(default_outfile, "JPEG")
    for i in range(0, iterations):
        infile = "compressed" + str(i) + ".jpg"
        outfile = "compressed" + str(i+1) + ".jpg"
        with Image.open(infile) as im:
            original_size = im.size
            current_dip = interpolated_dip(i, iterations, dip_percentage)
            print("saving" + outfile + " " + str(current_dip) + "%")

            im = im.resize((int(original_size[0]*current_dip/100), int(original_size[1]*current_dip/100)),
                           resample=PIL.Image.NEAREST)
            im = im.convert("YCbCr")
            im = im.resize(original_size)
            im = im.convert("RGB")
            images.append(im)
            im.save(outfile, "JPEG")
    return images


def make_gif(frames):
    frames[0].save("decay.gif", save_all=True, append_images=frames[1:], optimize=True)


if __name__ == '__main__':
    iterations = 400
    dip_percentage = 70
    frames = jpeg_blast_alien(iterations, dip_percentage)
    frames[-1].show()
    make_gif(frames)
