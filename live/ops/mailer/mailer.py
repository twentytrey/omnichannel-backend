import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mailer:
    def __init__(self,sender_email,receiver_email,subject,url,password):
        self.sender_email=sender_email
        self.receiver_email=receiver_email
        self.subject=subject
        self.url=url
        self.password=password
        
    def buildmessage(self):
        message=MIMEMultipart("alternative")
        message["Subject"]=self.subject
        message["From"]=self.sender_email
        message["To"]=self.receiver_email
        text = """\
        Hi,
        Following your sign up on Pronov,
        click the following link or copy it to your browser to confirm your registration and proceed:
        {0}""".format(self.url)
        html = """\
        <html>
        <body>
            <p>Hi,<br>
            Following your sign up on Pronov, click the following link or copy it to your browser to confirm your registration and proceed:<br>
            <a href="{0}">Confirm your account.</a> 
            </p>
        </body>
        </html>
        """.format(self.url)
        part1=MIMEText(text, "plain")
        part2=MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        context=ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email,self.password)
            server.sendmail(self.sender_email,self.receiver_email,message.as_string())

# if __name__=="__main__":
#     m=Mailer("pronovserver@gmail.com","jmsoyewale@gmail.com","Login details","http://localhost:8080/#/",'f10aeb05')
#     m.buildmessage()
