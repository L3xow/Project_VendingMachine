import cv2
import mediapipe as mp
import time


class poseDetector():

    def __init__(self, mode=False, upBody = False, smooth = True, detectionCon = 0.5, trackCon = 0.5):
        """
        Konstruktor für das Objekt der Klasse poseDetector. Hier werden gewisse Einstellungen bereits vorkonfiguriert.
        Dieses Objekt ist verantwortlich für die Kameraerkennung und festlegen/zeichnen der Landmarks.

        :param mode: (bool) : Default: False; True für statische Bilder, False für Videofeed.
        :param upBody: (bool) : Default: False; True für nur Oberkörper-Erkennung, False für gesamten Körper erkennen.
        :param smooth: (bool) : Default: True; True für flüssigere Erkennung, auf Kosten der Leistung
        :param detectionCon: (float) : Default: 0.5; DetectionConfidence, höher um stabilere Auswertung zu erreichen.
        :param trackCon: (float) : Default: 0.5; TrackingConfidence, höher um genauere Auswertung der Landmarks zu erreichen.
        """

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils


    def findPose(self, img, draw = True):
        """
        Funktion zum finden des Körpers und der erkennung der Landmarks/Gelenke.

        :param img: (object) : Image das von OpenCV eingelesen wird.
        :param draw: (bool) : Default: True; False wenn keine Punkte eingezeichnet werden sollen.
        :return: (object) : Gibt die eingezeichneten Punkte auf dem eingespeisten Videofeed wieder.
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if draw:
            if self.results.pose_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img


    def findPosition(self, img, draw=True):
        """
        Funktion zum erstellen des 3-dimensionalen Arrays. [0] = ID_Landmarks; [1] = x-Koordinate_Landmark;
        [2] = y-Koordinate_Landmark; [3] = Visibility_Landmark.

        :param img: (object) : Image das von OpenCV eingelesen wird.
        :param draw: (bool) : Default: True; False wenn keine Punkte eingezeichnet werden sollen.
        :return: (array) : 3D Array dass die Landmarks und Koordinaten enthält.
        """
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # Koordinaten müssen umberechnet werden, da Mediapipe einen Floatwert von 0.0 - 1.0 gibt,
                # der im Verhältnis zur Größe des Videos steht.
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy, lm.visibility*100])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList




def main():
    """
    Funktion zum testen und debuggen der Kameraauswertung. Somit kann PoseModule auch unabhängig von
    mainwindow ausgeführt werden und getestet werden.

    :return:
    """
    cap = cv2.VideoCapture(0)
    pTime = 0
    count = 0
    check = False

    detector = poseDetector()

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[27][0])
            if lmList[27][3] > 95 and lmList[28][3] > 95 and lmList[23][1] < 380 and lmList[24][1] > 270:
                print(lmList[23][0])
                print(lmList[24][0])
                if count < 50:
                    if lmList[15][1] < 420 and lmList[15][2] > 240 and lmList[16][1] > 250 and lmList[16][2] > 240 and not check:  # [Teil][x] < X_WERT         [Teil][Y] < Y_WERT #ruhe
                        check = True
                        count += 1
                        print(check)
                        print(count)
                    if lmList[15][1] > 500 and lmList[15][2] < 150 and lmList[16][1] < 150 and lmList[16][2] < 150 and check:          #work
                        check = False
                        count += 1
                        print(check)
                        print(count)


        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(10)


if __name__ == "__main__":
    main()