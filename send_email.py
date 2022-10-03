import smtplib
from email.mime.text import MIMEText

def sendemail(email, height, avereage_height, count):
    # fake email and password
    from_email="myemail@gmail.com"
    from_password="mypassword"
    to_email=email

    subject = "Report about Your Height"
    content = "Your height is <b>%s</b>. And average height of all is %s. Beside, the total amount of participated people is %s." % (height, avereage_height, count)

    msg = MIMEText(content, 'html')  # content will be read as a html
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email
    print(msg['Subject'])

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_psw)
    gmail.send_message(msg)
