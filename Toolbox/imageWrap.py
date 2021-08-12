from PIL import Image

def readImage(dirBaseNameImage):
    return Image.open(dirBaseNameImage)

def readImages(dirBaseNameImageList):
    return list(readImage(dir) for dir in dirBaseNameImageList)

def saveImage(img, dirBaseNameImage):
    img.save(dirBaseNameImage+'.jpg')
    
def saveImages(imgList, dirName, names = None):
    if not names:
        names = range(len(imgList))
    for index, baseName in enumerate(names):
        saveImage(imgList[index], os.path.join(dirName, baseName))

def get_concat_h_blank(im1, im2, color=(255, 255, 255)):
    dst = Image.new('RGB', (im1.width + im2.width, max(im1.height, im2.height)), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v_blank(im1, im2, color=(255, 255, 255)):
    dst = Image.new('RGB', (max(im1.width, im2.width), im1.height + im2.height), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def get_concat_h_multi(im_list):
    _im = im_list.pop(0)
    for im in im_list:
        _im = get_concat_h_blank(_im, im)
    return _im

def get_concat_v_multi(im_list):
    _im = im_list.pop(0)
    for im in im_list:
        _im = get_concat_v_blank(_im, im)
    return _im