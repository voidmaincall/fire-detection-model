
import cv2         # Library for openCV
import threading   # Library for threading -- which allows code to run in backend
import pygame      # Library for alarm sound
# import yagmail     # Library for email sending
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml') # To access xml file which includes positive and negative images of fire. (Trained images)

vid = cv2.VideoCapture(0) # To start camera this command is used "0" for laptop inbuilt camera and "1" for USB attached camera
runOnce = False # created boolean
runOnce1 = False # created boolean

# Initialize pygame mixer
pygame.mixer.init()

def play_alarm_sound_function(): # defined function to play alarm post fire detection using threading
    global runOnce
    pygame.mixer.music.load('fire_alarm.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    print("Fire alarm end") # to print in console
    runOnce = False # Reset the flag after the sound finishes playing

def send_mail_function(): # defined function to send mail post fire detection using threading
    global runOnce1
    recipientmail = "arsh.jain2003@gmail.com" # recipient's mail
    sender_email = "arsh.jain2004@gmail.com"
    sender_password = 'rfee lsfm zwsa ddqb'
    
    subject = "Fire Alert"
    body = "Warning: A fire accident has been reported."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipientmail
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        print("Server started")
        server.ehlo()
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipientmail, text)
        print("Alert mail sent successfully to {}".format(recipientmail)) # to print in console to whom mail is sent
        server.close() # To close server
        
    except Exception as e:
        print(e) # To print error if any
    runOnce1 = False # Reset the flag after the email is sent

while(True):
    ret, frame = vid.read() # Value in ret is True, to read video frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # To convert frame into gray color
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5) # to provide frame resolution

    ## to highlight fire with a square 
    for (x,y,w,h) in fire:
        cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        if runOnce == False:
            print("Fire alarm initiated")
            threading.Thread(target=play_alarm_sound_function).start()  # To call alarm thread
            runOnce = True
        
        if runOnce1 == False:
            print("Mail sent initiated")
            threading.Thread(target=send_mail_function).start() # To call mail thread
            runOnce1 = True

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
