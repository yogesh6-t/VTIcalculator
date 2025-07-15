import torch
import cv2
import os
import tarfile
import yaml
import shutil
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import ultralytics 
from ultralytics import YOLO
import pytesseract

best_model_path = r"F:\ECG\medical science\runs\detect\train\weights\best.pt"
save_dir = r'F:\ECG\medical science\vti\models\\'
os.makedirs(save_dir, exist_ok=True)

shutil.copy(best_model_path, os.path.join(save_dir, 'my_trained_yolo_model.pt'))

print(f"Model saved to {save_dir}")

SCREEN_WIDTH = 400 #mm
SCREEN_RES = 720 #px
SWEEP_SPEED = 225 #mm/s
print('SWEEP_SPEED : ', SWEEP_SPEED)
TIME_PER_PX = 1/(SWEEP_SPEED * (SCREEN_RES/SCREEN_RES))
kernel_d = np.ones((3,3), np.uint8)
#for verification
vmax_dict = {'test1.jpg': [45,60,235,320], 'test2.jpg': [7,13,7,53],
             'test5.jpg': [96,114,13,145], 'test7.jpg': [45,60,235,320]}

expected_vti = {'test1.jpg': 14.5, 'test2.jpg': 15.3,
                'test5.jpg': 19.7, 'test7.jpg': 22.6}
vti_lst =[]
model = YOLO(r'F:\ECG\medical science\vti\models\my_trained_yolo_model.pt')

# Path to the test image
test_image = r'F:\ECG\medical science\vti\vti\images\val\test2.jpg'

img = cv2.imread(test_image)
# Run inference
results = model(test_image)

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
imgbw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
vmax = pytesseract.image_to_string(imgbw[vmax_dict.get(os.path.basename(test_image))[0]:vmax_dict.get(os.path.basename(test_image))[1],
                                         vmax_dict.get(os.path.basename(test_image))[2]:vmax_dict.get(os.path.basename(test_image))[3]],
                                   lang='eng', config='--psm 13')
##plt.imshow(imgbw, cmap=plt.cm.binary)
##plt.show()
cv2.imshow('VMAX', imgbw[vmax_dict.get(os.path.basename(test_image))[0]:vmax_dict.get(os.path.basename(test_image))[1],
                         vmax_dict.get(os.path.basename(test_image))[2]:vmax_dict.get(os.path.basename(test_image))[3]])
Vmax=''
for i in vmax:
    if i.isnumeric():
        Vmax += i
print(f'vmax : {vmax}')
Vmax = float(Vmax)

# Add bounding boxes
for i,result in enumerate(results):
    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()  # Get box coordinates
        conf = box.conf[0].cpu().numpy()            # Confidence score
        cls = int(box.cls[0].cpu().numpy())         # Class index
        img_snip = imgbw[int(y1):int(y2), int(x1):int(x2)]
        TOTAL_TIME = TIME_PER_PX * int(x2-x1)
        print(str(TOTAL_TIME) + 'ms')
        _, thresh1 = cv2.threshold(img_snip, 60, 255, cv2.THRESH_BINARY)
        dilated1 = cv2.dilate(thresh1, kernel_d, iterations=1)
        contours1, _ = cv2.findContours(dilated1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        vti_contour = max(contours1, key=cv2.contourArea)
        area1 = cv2.contourArea(vti_contour)
        cv2.drawContours(imgbw[int(y2):int(y1), int(x1):int(x2)], [vti_contour], -1, (0, 0, 255), 2)
        VTI1 = round((area1*Vmax*TOTAL_TIME)/(int(x2-x1)*int(y2-y1)), 2)
        vti_lst.append(VTI1)
        cv2.putText(imgbw, 'VTI:' + str(VTI1)+ 'cm', (170, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        rect = plt.Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, color='red', linewidth=2)
        plt.gca().add_patch(rect)
        plt.text(x1, y1-10, f'VTI:{VTI1}', color='red', fontsize=12)

EXPECTED_VTI = expected_vti.get(os.path.basename(test_image))
print('EXPECTED_VTI', EXPECTED_VTI)
print('vti_lst', vti_lst)
print(f'average VTI {os.path.basename(test_image)} : {round(sum(vti_lst)/len(vti_lst),2)} cm')
print(f'error {os.path.basename(test_image)} : {round((round(sum(vti_lst)/len(vti_lst),2) - EXPECTED_VTI)*100/EXPECTED_VTI,2)}%')
plt.axis('off')
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
