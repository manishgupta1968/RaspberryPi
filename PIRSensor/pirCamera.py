import RPi.GPIO as GPIO
import smtplib, string, subprocess, time
#import picamera
import datetime
import picamera
# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from subprocess import call 


SSL_PORT='465'
SMTP_USERNAME = 'manishgupta1968@gmail.com'	#Mail id of the sender
SMTP_PASSWORD = 'expl0reg00gle'	#Pasword of the sender
SMTP_RECIPIENT = 'gmanish@in.ibm.com'	#Mail id of the reciever
SMTP_SERVER = 'smtp.gmail.com'
print( "working")



# Logic to detect motion and then send out a picture
sensor = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)
camera = picamera.PiCamera()

previous_state = False
current_state = False
while True:
    time.sleep(0.1)
    previous_state = current_state
    current_state = GPIO.input(sensor)
    if current_state != previous_state:
        new_state = "HIGH" if current_state else "LOW"
        print("GPIO pin %s is %s" % (sensor, new_state))
        camera.capture('image.jpg')
        # Create the container (outer) email message.
        TO = SMTP_RECIPIENT
        FROM = SMTP_USERNAME
        msg = MIMEMultipart()
        msg.preamble = 'Rpi Semds image'
        fp = open('image.jpg', 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)        
        # Send the email via Gmail.
        print ("Sending the mail")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SSL_PORT)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(FROM, [TO], msg.as_string())
        server.quit()
        print ("Mail sent" )
