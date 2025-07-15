import cv2
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread(r'D:\Docs\ECG\testy2.jpg', cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread(r'D:\Docs\ECG\test1.jpg', cv2.IMREAD_GRAYSCALE)
blurred = cv2.GaussianBlur(image, (3, 3), 0)
edges = cv2.Canny(blurred, 50, 150)
dilated = cv2.dilate(edges, kernel = np.ones((3,3), np.uint8), iterations=1)

##plt.imshow(image2, cmap='gray')
##plt.title("dilated Image")
##plt.show()
##cv2.imshow('img1', edges)

y_projection = np.sum(dilated, axis=1)  # Sum along X-axis
##plt.plot(y_projection)
##plt.title("Y-axis Projection Profile")
##plt.show()
cv2.imshow('img2', dilated)

from scipy.signal import find_peaks
# Example: detect tick marks on the X-axis
peaks_y, _ = find_peaks(y_projection, height=100)
##print("X tick pixel positions:", peaks_y)

# Measure pixel distances between tick marks
pixel_distances = np.diff(peaks_y)
##print("Estimated pixel distance between ticks:", pixel_distances)
print(f"Estimated pixel distance between ticks:{max(pixel_distances)} pxs")

##cv2.waitKey(0)
##cv2.destroyAllWindows()
