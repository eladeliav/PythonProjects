import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while cv2.waitKey(1) != ord('q'):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([150, 150, 50])
    upper = np.array([180, 255, 150])

    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("frame", frame)
    cv2.imshow("result", result)

cap.release()
cv2.destroyAllWindows()
