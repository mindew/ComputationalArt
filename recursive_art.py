""" This code generates the computational arts. Movie generator
    renders images that are generated from generate_art as a video.
    Now uses OpenCV2 as movie generation. Creating computational Art
    by using this code is required before creating a video
    Created by Minju Kang"""

import random
import math
from PIL import Image
import numpy
import cv2

x_size = 350
y_size = 350


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    functions = ["prod", "avg", "cos_pi", "sin_pi", "cube", "square", "x", "y"]
    depth = random.randint(min_depth, max_depth)
    # randomly generates the depth value between min_depth and max_depth
    if depth == 1:
        return random.choice(functions[6:7])
        # randomly select string between x or y
    return[random.choice(functions[0:6]), build_random_function(depth-1, depth-1), build_random_function(depth-1, depth-1)]
    # returns randomly generated function represented as a nested list


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    for item in f:
        if item == "x":
            return x
        elif item == "y":
            return y
        elif item == "prod":
            return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
            # multiply x and y
        elif item == "avg":
            return 0.5 * ((evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y)))
        elif item == "cos_pi":
            return math.cos(math.pi*(evaluate_random_function(f[1], x, y)))
        elif item == "sin_pi":
            return math.sin(math.pi*(evaluate_random_function(f[1], x, y)))
        elif item == "cube":
            return (evaluate_random_function(f[1], x, y))**3
        elif item == "square":
            return (evaluate_random_function(f[1], x, y))**2
        else:
            return -1
    return -1


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    dInput = input_interval_start - input_interval_end
    dOutput = output_interval_start - output_interval_end
    slope = dOutput/dInput
    res = slope*(val-input_interval_start) + output_interval_start
    return res


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


# def generate_movie(filename, x_size=350, y_size=350):
#     movielist = []
#     for j in range(0, 50):
#         movielist.append(random.randint(1, 10))
#         for k in range(0, 5):
#             img = movielist[k]
#             generate_art(filename, x_size, y_size, img)


def generate_art(filename, x_size, y_size):
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    # red is the function of x
    green_function = build_random_function(7, 9)
    # green is the function of y
    blue_function = build_random_function(7, 9)
    # blue is the function of x
    im = Image.new("RGB", (x_size, y_size))
    # "RGB" indicates that the image has three color channels
    pixels = im.load()
    # im.load command returns a pixel access object
    for i in range(x_size):
        for j in range(y_size):
            # nested for loops create each pixel value based on evaluationg
            # the red, green and blue channel functions
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            # the functions we will be generating have inputs
            # in the interval [-1,+1] and outputs in the interval[-1,+1]
            # remap interval remaps [0.349]to the values between [-1,+1]
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )
            # evaluates each the red, green,and blue channel functions
            # to obtain the intensity for each color channel for the pixe(i,j)
    im.save(filename)
    # saves the image to disk as specified filename("myart.png")


def generate_movie():
    """ blends the image and then released blended image as movie"""
    # load the pre-saved images that are generated from generate_art
    image1 = Image.open("myart1.png")
    image2 = Image.open("myart2.png")
    image3 = Image.open("myart3.png")
    image4 = Image.open("myart4.png")
    image5 = Image.open("myart5.png")

    # since all images have same height, width, layers, grab the shape from any image
    height, width, layers = numpy.array(image1).shape

    # create a video by using cv2
    # looked after cv2 documentation
    video = cv2.VideoWriter("my_movie", -1, 10, (width, height))

    # merge the images
    for i in range(0, 30):
        # 30 frames for transition. 30 / 10 = 3 seconds for transition between two images
        images1And2 = Image.blend(image1, image2, i/30.0)
        video.write(cv2.cvtColor(numpy.array(images1And2), cv2.COLOR_RGB2BGR))
        # and repeat the for loop for each image

    for i in range(0, 30):
        images2And3 = Image.blend(image2, image3, i/30.0)
        video.write(cv2.cvtColor(numpy.array(images2And3), cv2.COLOR_RGB2BGR))

    for i in range(0, 30):
        images3And4 = Image.blend(image3, image4, i/30.0)
        video.write(cv2.cvtColor(numpy.array(images3And4), cv2.COLOR_RGB2BGR))

    for i in range(0, 30):
        images4And5 = Image.blend(image4, image5, i/30.0)
        video.write(cv2.cvtColor(numpy.array(images4And5), cv2.COLOR_RGB2BGR))

    # return to image 1
    for i in range(0, 30):
        images5And1 = Image.blend(image5, image1, i/30.0)
        video.write(cv2.cvtColor(numpy.array(images5And1), cv2.COLOR_RGB2BGR))

    # release the video
    video.release()


if __name__ == '__main__':
    generate_movie()
