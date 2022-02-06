import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

def roi(img, show=True):
  # ROI from the center
  img = img * 255
  H, W = img.shape
  w = 100
  h = 170
  oy = int(H / 2) - 52
  ox = int(W / 2) - 40
  y = oy
  Y = y + h
  x = ox
  X = x + w
  img = img[y:Y, x:X]
  if show:
    plt.axis('off')
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.show()
  return img

def hist(img):
  # import ipdb; ipdb.set_trace() # minimim pixel value 16, probably because of the gain value
  img = img.reshape((img.size,)) * 255
  bins = np.arange(256)
  h = np.histogram(img, bins)
  plt.hist(img, bins)
  plt.show()

under = mpimg.imread("under.png")
# roi(under)
hist(under)

good = mpimg.imread("good.png")
hist(good)

over = mpimg.imread("over.png")
hist(over)


