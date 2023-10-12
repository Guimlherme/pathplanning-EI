import cv2
import numpy as np
from constants import ONE_LINE_MAP,MINIMUM_AREA,DISTANCE_BETWEEN_LINES

def preprocessing_one_line(image,save_photos=False):
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

def preprocessing_two_lines(image,save_photos=False):

  # Cropping image
  image = image[int(0.6*image.shape[0]):int(0.99*image.shape[0]),int(0.00*image.shape[1]):int(1*image.shape[1])]

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
  lower= np.array([0, 0, 190])
  upper = np.array([179, 27, 255])
  mask = cv2.inRange(hsv, lower, upper)

  # Remove noise
  kernel_erode = np.ones((5,5), np.uint8)
  eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
  kernel_dilate = np.ones((4,4), np.uint8)
  dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)
  cv2.imwrite('image.png',image)
  cv2.imwrite('mask.png',dilated_mask)

  # Find the different contours
  _, contours, hierarchy = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

  # Sort by area (keep only the biggest one)
  contours = sorted(contours, key=cv2.contourArea, reverse=True)
  
  psi = 0
  
  if len(contours)>0:

      if cv2.contourArea(contours[0])>MINIMUM_AREA:

        if len(contours)>1 and cv2.contourArea(contours[1])>MINIMUM_AREA:
          cx_mean = []
          cy_mean = []
          for i in range(2):
            M = cv2.moments(contours[i])
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cx_mean.append(cx)
            cy_mean.append(cy)
          cx_mean = int(np.mean(cx_mean))
          cy_mean = int(np.mean(cy_mean))
        else:
          M = cv2.moments(contours[0])
          cx = int(M['m10']/M['m00'])
          cy = int(M['m01']/M['m00'])

          if cx > (width/2):
            cx_mean = int(min(max(0,cx - (DISTANCE_BETWEEN_LINES/2)),width))
            cy_mean = cy
          else:
            cx_mean = int(min(max(0,cx + (DISTANCE_BETWEEN_LINES/2)),width))
            cy_mean = cy

        if save_photos:
            cv2.circle(resized, (cx_mean, cy_mean), 5, (255, 0, 0), -1)
            cv2.circle(resized, (int(width/2), height), 3, (0, 0, 255), -1)
            for contour in contours:
              cv2.drawContours(resized, contour, -1, (0, 255, 0), 5)
            cv2.imwrite('countours.png',resized)
            cv2.imwrite('mask.png',dilated_mask)

        psi = np.arctan((cx_mean-(width/2))/(height-cy_mean))
            
  return psi
    

def preprocessing_image(image,save_photos=False):
  if ONE_LINE_MAP:
    return preprocessing_one_line(image,save_photos)
  else:
    return preprocessing_two_lines(image,save_photos)
