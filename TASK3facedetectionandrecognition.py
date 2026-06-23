import cv2, os, pickle
import numpy as np
from pathlib import Path

hc = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
ec = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_eye.xml')

def dt(f):
    img = cv2.imread(f)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = hc.detectMultiScale(gray, 1.1, 4)
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        eyes = ec.detectMultiScale(gray[y:y+h, x:x+w])
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(img, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (255,0,0), 2)
    
    cv2.imwrite('detected_'+Path(f).name, img)
    print(f"Detected {len(faces)} face(s) - Saved: detected_{Path(f).name}")

def w_cam():
    cap = cv2.VideoCapture(0)
    print("\n🎥 Webcam Active (Press 'q' to quit, 's' to save face)")
    
    while True:
        ret, f = cap.read()
        if not ret: break
        
        gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        faces = hc.detectMultiScale(gray, 1.1, 4)
        
        for (x,y,w,h) in faces:
            cv2.rectangle(f, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(f, 'Face', (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            
            eyes = ec.detectMultiScale(gray[y:y+h, x:x+w])
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(f, (x+ex,y+ey), (x+ex+ew,y+ey+eh), (255,0,0), 2)
        
        cv2.putText(f, f'Faces: {len(faces)}', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.imshow('Face Detection', f)
        
        k = cv2.waitKey(1) & 0xFF
        if k==ord('q'): break
        if k==ord('s') and len(faces)>0:
            x,y,w,h = faces[0]
            face_img = f[y:y+h, x:x+w]
            cv2.imwrite(f'saved_face_{len(os.listdir("."))}.jpg', face_img)
            print("Face saved!")
    
    cap.release()
    cv2.destroyAllWindows()

def e_faces(d):
    if not os.path.exists(d):
        print(f"Directory {d} not found!")
        return {}
    
    enc = {}
    for p in os.listdir(d):
        path = os.path.join(d, p)
        if os.path.isfile(path):
            img = cv2.imread(path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = hc.detectMultiScale(gray, 1.1, 4)
            if len(faces)>0:
                x,y,w,h = faces[0]
                enc[p] = img[y:y+h, x:x+w]
    
    return enc

def rec_f(f_img, enc_dict):
    best_m = None
    best_s = 0.5
    
    for name, face_enc in enc_dict.items():
        if f_img.shape != face_enc.shape:
            face_enc = cv2.resize(face_enc, (f_img.shape[1], f_img.shape[0]))
        
        diff = cv2.matchTemplate(f_img, face_enc, cv2.TM_CCOEFF)
        if diff > best_s:
            best_s = diff
            best_m = name.split('.')[0]
    
    return best_m if best_s>0.5 else "Unknown"

def menu():
    print("\n" + "="*50)
    print("FACE DETECTION & RECOGNITION")
    print("="*50)
    print("1. Detect faces in image")
    print("2. Live webcam detection")
    print("3. Recognize faces from training")
    print("4. Exit")
    print("="*50)

def main():
    while True:
        menu()
        c = input("\nChoose (1-4): ").strip()
        
        if c=='1':
            f = input("Enter image path: ").strip()
            if os.path.exists(f):
                dt(f)
            else:
                print("File not found!")
        
        elif c=='2':
            w_cam()
        
        elif c=='3':
            train_dir = input("Enter training faces directory: ").strip()
            enc = e_faces(train_dir)
            if enc:
                print(f"Loaded {len(enc)} reference faces")
                test_img = input("Enter test image path: ").strip()
                if os.path.exists(test_img):
                    img = cv2.imread(test_img)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = hc.detectMultiScale(gray, 1.1, 4)
                    
                    if len(faces)>0:
                        x,y,w,h = faces[0]
                        face = img[y:y+h, x:x+w]
                        name = rec_f(face, enc)
                        print(f"👤 Match: {name}")
                    else:
                        print("No face detected!")
            else:
                print("No faces in directory!")
        
        elif c=='4':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()