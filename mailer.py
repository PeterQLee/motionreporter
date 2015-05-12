import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  # Added
from email.mime.image import MIMEImage

class Mailer:
    
    def __init__(self,hostaddr,hostpass):
        self.hostpass=hostpass
        self.hostaddr=hostaddr
    def send_email(self,rec,image):
        import smtplib
        
        gmail_user = "serverhomework@gmail.com"#"jimjang.jambles@gmail.com"
        gmail_pwd = "charleyhorsewheel"#"waterbowl9tube"
        FROM = gmail_user#'jimjang.jambles@gmail.com'
        TO = rec #must be a list
        SUBJECT = "AMBER HOUSE ALLERT"
        TEXT = 'Your house is being broken into, come back '
        msg=MIMEMultipart()
        msgText=MIMEText(TEXT)
        msg["To"]=TO
        msg["From"]=FROM
        msg["Subject"]=SUBJECT

        
        
        #msg.preamble="ayyy"
        msg.attach(msgText)
        img=MIMEImage(image)
        img.add_header("Content-ID","inline",filename="intruder")
        
        msg.attach(img)
       
        
    # Prepare actual message
        #message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
   # """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
                #server = smtplib.SMTP(SERVER)
            server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, msg.as_string())
                #server.quit()
            server.close()
            
        except:
            print ("Error sending alert email!")
            raise
