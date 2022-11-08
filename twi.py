import os
from twilio.rest import Client
import random

account_sid = 'AC18db6a7dc294b86c6c1efa29b67493f1'
auth_token = "6166a800a69d4d3a90ebab255d5e3ba2"
client = Client(account_sid, auth_token)

otp = random.randint(1111,9999)
message = client.messages \
                .create(
                     body=" AXIS BANK INR 20000.00 Debited from A/c no. XX098765 31-10-2022 15:36:50 ATM_WDL/AXIS BANK SMS BLOCKCARD 0048 to +918691000002, if not done by you- contact   ",
                    # body="Otp is :"+str(otp),
                     from_='+19702870724',
                     to='+919834838406'
                 )

print(message.sid)