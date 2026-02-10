# import smtplib
# from twilio.rest import Client

# def send_email(to,msg):
#     s=smtplib.SMTP("smtp.gmail.com",587)
#     s.starttls()
#     s.login("your@gmail.com","APP_PASSWORD")
#     s.sendmail("your@gmail.com",to,msg)
#     s.quit()

# def send_sms(to,msg):
#     client=Client("TWILIO_SID","TWILIO_TOKEN")
#     client.messages.create(body=msg,from_="+123456789",to=to)
def send_email(to, msg):
    print(f"EMAIL → {to} : {msg}")

def send_sms(to, msg):
    print(f"SMS → {to} : {msg}")
