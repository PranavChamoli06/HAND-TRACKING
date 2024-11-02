import cv2
import mediapipe as mp
import time

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

ptime = 0

while True:
    success, img = cap.read()
    
    if not success:
        break  # Exit the loop if frame is not captured

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id , lm in enumerate(handLms.landmark):
                #print(id , lm)
                h , w , c = img.shape
                cx , cy = int(lm.x*w ) ,  int(lm.y*h)
                print(id , cx , cy)
                
                if id in [0, 4, 8, 12, 16, 20]:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            # Draw landmarks for each detected hand
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


    ctime = time.time()
    fps = 1 / (ctime-ptime)
    ptime = ctime
    
    cv2.putText(img , str(int(fps)) , (10,70) , cv2.FONT_HERSHEY_COMPLEX , 1 , (255 , 0 , 0) , 3)
    cv2.imshow("Img", img)
    
    # Check if the OpenCV window was closed
    if cv2.getWindowProperty("Img", cv2.WND_PROP_VISIBLE) < 1:
        break
    
    # Alternatively, press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
