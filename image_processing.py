

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])


def visual_validation(image):
    title = str(image.rstrip(".png"))
    image = misc.imread(image)
    image = rgb2gray(image)
    mask = image > image.mean()
    blob_labels = measure.label(mask,background=0)
    fig, ax = plt.subplots(figsize=(4, 3))
    plt.title(str(title))
    ax.imshow(mask, cmap=plt.cm.spectral, interpolation='nearest')
    plt.show()


def image_process(image,variant,right_number):

    image_name = image.rstrip(".png")
    image = misc.imread(image)
    image = rgb2gray(image)
    mask = image > image.mean()
    blob_labels = measure.label(mask,background=0)
    properties = measure.regionprops(blob_labels)

    number = len(properties)

    if number == len(properties):
        print "Everything is correct!"
    else:
        print "Invalid"
    area_1 = []
    for i in properties:
        area_1.append(i.area)

    with open(str(image_name)+"_"+variant+".csv","w") as f:
        for i in properties:
            f.write(str(i.area)+","+str(sqrt(i.equivalent_diameter/2)*pi)+","+str(i.equivalent_diameter*100/520)+"\n")
    print "Check the file!"
    return sum(area_1)






if __name__ == "__main__":

    import os
    from time import gmtime, strftime
    import sys
    import argparse
    from skimage import data, io, filters
    from scipy import misc
    from scipy import ndimage
    import matplotlib.pyplot as plt
    from skimage import measure
    from skimage import data
    from skimage import filters
    import numpy as np
    from skimage import morphology
    from skimage.feature import peak_local_max
    from skimage.morphology import watershed
    import scipy.ndimage as ndi
    from skimage.filters import sobel
    from skimage.feature import canny
    from math import pi
    from math import sqrt

    description = """

Version 1.0

If you have any questions, please do not hesitate to contact me
email address: michal.karlicki@gmail.com
"""

    epilog = """

"""


    parser = argparse.ArgumentParser(
                    description=description,
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    epilog=epilog)


    parser.add_argument('image_1', metavar='image_1', type=str)
    parser.add_argument('variant_1', metavar='variant_1', type=str)
    parser.add_argument('right_number_1', metavar='right_number_1', type=str)
    parser.add_argument('image_2', metavar='image_2', type=str)
    parser.add_argument('variant_2', metavar='variant_2', type=str)
    parser.add_argument('right_number_2', metavar='right_number_2', type=str)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    start = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    visual_validation(args.image_1)
    visual_validation(args.image_2)
    image_c = image_process(args.image_1,args.variant_1,args.right_number_1)
    image_z = image_process(args.image_2,args.variant_2,args.right_number_2)

    with open("ratio_"+str(args.image_1).strip(".png"),"w") as f:
        f.write(str(image_c/(float(image_c)+image_z) * 100.0))

    print "The percentege is "+str(image_c/(float(image_c)+image_z) * 100.0)


    end = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    print "Starting time: "+start
    print "Ending time: "+end
