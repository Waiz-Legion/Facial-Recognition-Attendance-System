import cv2
import datetime as dt
import pandas as pd
import csv
#import datetime as dt
import os
def recog_n_save(subject):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    def attRecord(ids, sub):
        now = dt.datetime.now()
        time = now.strftime('%I:%M:%S:%p')
        date = now.strftime('%d-%B-%Y')
        weekday = now.strftime('%A')
        sub = subject
        record = [ids, time, date, weekday, subject]
        
        file_exists = os.path.isfile('data.csv')
        # Open the CSV file in write mode with newline=''
        with open('data.csv', 'a', newline='') as file:

            # Create a writer object
            writer = csv.writer(file)
            if not file_exists:
                # Write the header row
                writer.writerow(['Roll Number', 'Time', 'Date', 'Weekday', 'Subject'])

            # Write the record to the CSV file
            writer.writerow(record)
        df = pd.read_csv('data.csv')
        df.drop_duplicates(subset = ['Roll Number'], inplace = True)
        df = df.drop(df.loc[df['Roll Number'] == 0].index)
        df = df.drop(df.loc[df['Roll Number'] == 'unknown'].index)
        df.to_csv('data.csv', index = False)
        
    font = cv2.FONT_HERSHEY_SIMPLEX

    id = 0
    names = []

    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    #cam.set(cv2.CAP_PROP_FPS, 1)

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    duration = 4  # in seconds

    # Start the timer
    start_time = cv2.getTickCount()

    # Read frames from the camera until the timer reaches the duration
    while ((cv2.getTickCount() - start_time) / cv2.getTickFrequency()) < duration:       

        ret, img = cam.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            if confidence < 100:
                # id = names[id]
                confidence = "  {0}%".format(round(confidence))

            else:
                id = "unknown"
                confidence = "  {0}%".format(round(confidence-100))

            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)
        #print(img[-1])
        attRecord(id, subject)
        
        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break
    print('Record saved successfully')
    print("\n [INFO] Exiting Program")
    cam.release()
    cv2.destroyAllWindows()
