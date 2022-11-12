import cv2
import numpy as np


def preprocessing_image(image,save_photos=False):
  # Cropping image

  image = image[int(0.4 * image.shape[0]):int(0.99 * image.shape[0]),
          int(0.15 * image.shape[1]):int(0.75 * image.shape[1])]

  # Reescalling
  scale_percent = 30 # percent of original size
  width = int(image.shape[1] * scale_percent / 100)
  height = int(image.shape[0] * scale_percent / 100)
  dim = (width, height)

  resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

  # Convert to HSV color space

  blur = cv2.blur(resized,(5,5))
  ret,thresh1 = cv2.threshold(blur,168,255,cv2.THRESH_BINARY)
  hsv = cv2.cvtColor(thresh1, cv2.COLOR_RGB2HSV)

  # Define range of white color in HSV
  #hue (matiz), saturation (saturação) e value (valor)
  lower= np.array([0, 0, 164])
  upper = np.array([179, 27, 255])
  mask = cv2.inRange(hsv, lower, upper)

  # Remove noise
  kernel_erode = np.ones((5,5), np.uint8)
  eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
  kernel_dilate = np.ones((4,4), np.uint8)
  dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)


  # Find the different contours
  res = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  if len(res) == 2:
    contours, hierarchy = res
  else:
    _, contours, hierarchy = res
  # Sort by area (keep only the biggest one)
  contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

  if len(contours) > 0:
      M = cv2.moments(contours[0])
      cx = int(M['m10']/M['m00'])
      cy = int(M['m01']/M['m00'])


      if save_photos:
        cv2.circle(resized, (cx, cy), 5, (255, 0, 0), -1)
        for contour in contours:
          cv2.drawContours(resized, contour, -1, (0, 255, 0), 10)
        cv2.imwrite('contours.png',resized)
        cv2.imwrite('mask.png',dilated_mask)


      theta = np.arctan((cx-(width/2))/(height-cy))
      return theta

  else:
      return 0