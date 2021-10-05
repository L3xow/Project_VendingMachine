import cv2
import mediapipe as mp
import time
import math


class poseDetector():
    """
    Dient zur Auswertung des KameraInputs. Zuerst wird das Farbspektrum von RGB zu BGR gewandelt.
    Anschließend wird das gewandelte Bild an den Algorithmus von Mediapipe überreicht, welcher dann die sog. Landmarks
    einzeichnet und zurückgibt. Dazu erhalten wir ein Array bestehend aus den Landmark IDs und deren x, y und visibility
    Werten. Diese können nun verwendet werden, um bestimmte Bewegungen zu erkennen.

    """

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


def cosine_law(a, b, c):
    return math.degrees(math.acos((c**2 - b**2 - a**2)/(-2.0 * a * b)))

def precalcs(lm1, lm2, lm3, lmList):
    foot_x, foot_y = lmList[lm1][1], lmList[lm1][2]
    knee_x, knee_y = lmList[lm2][1], lmList[lm2][2]
    waist_x, waist_y = lmList[lm3][1], lmList[lm3][2]

    a_shin = foot_x - knee_x
    b_shin = foot_y - knee_y
    a_shin = abs(a_shin)
    b_shin = abs(b_shin)

    shinlen = math.hypot(a_shin, b_shin)

    a_thigh = knee_x - waist_x
    b_thigh = knee_y - waist_y
    a_thigh = abs(a_thigh)
    b_thigh = abs(b_thigh)

    thighlen = math.hypot(a_thigh, b_thigh)

    a_leg = foot_x - waist_x
    b_leg = foot_y - waist_y
    a_leg = abs(a_leg)
    b_leg = abs(b_leg)

    leglen = math.hypot(a_leg, b_leg)

    return cosine_law(shinlen, thighlen, leglen)


def main():
    """
    Funktion zum testen und debuggen der Kameraauswertung. Somit kann PoseModule auch unabhängig von
    mainwindow ausgeführt werden und getestet werden.

    :return:
    """
    cap = cv2.VideoCapture(1)
    pTime = 0
    count = 0
    check = False

    detector = poseDetector()

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:

            leftangle = precalcs(28, 26, 24, lmList)
            rightangle = precalcs(27, 25, 23, lmList)
            # print("left: ", leftangle)
            # print("right: ", rightangle)




            if True:
                # print(lmList[23][0])
                # print(lmList[24][0])
                if count < 50:
                    if leftangle > 130 and rightangle > 130 and not check:  # [Teil][x] < X_WERT         [Teil][Y] < Y_WERT #ruhe
                        check = True
                        count += 1
                        # print(check)
                        print(count)
                    if leftangle < 60 and rightangle < 60 and check:          #work
                        check = False
                        count += 1
                        # print(check)
                        print(count)


        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(10)


if __name__ == "__main__":
    main()