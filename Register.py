#// connect mariadb in pytho
# from flask.ext.login import LoginManager
# from flask_module import LoginManager
# login_manager = LoginManager()
# login_manager.init_app(app)
# import mariadb
# import sys
from flask import request, url_for, redirect
from email.policy import default
from flask import Flask, request, jsonify, make_response    
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
# import os
from twilio.rest import Client
import random
import redis
import ast



account_sid = 'AC18db6a7dc294b86c6c1efa29b67493f1'
auth_token = "6166a800a69d4d3a90ebab255d5e3ba2"
client = Client(account_sid, auth_token)




# POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)
POOL = redis.Redis(
    host= '172.16.0.76',
    port= '6379')
print("REdis connection success", POOL)

# def getVariable(variable_name):
#     my_server = redis.Redis(connection_pool=POOL)
#     response = my_server.get(variable_name)
#     return response

# def setVariable(variable_name, variable_value):
#     my_server = redis.Redis(connection_pool=POOL)
#     my_server.set(variable_name, variable_value)




app = Flask(__name__)
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://tracker:tracker@localhost:3306/Track")
print("Success")

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String(length=100))
    password = sqlalchemy.Column(sqlalchemy.String(length=20))
    mobile = sqlalchemy.Column(sqlalchemy.String(length=10))
    email = sqlalchemy.Column(sqlalchemy.String(length=100))
    otp = sqlalchemy.Column(sqlalchemy.String(length=4))
    active = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


#Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
Session = Session()

@app.route('/')
def home():
   return render_template('register.html')


@app.route('/register', methods =['POST'])
def register():
    if request.method == "POST":
        print(request.data,"BBBBBBBBBBBBBBBBBBBBB")
        Username = request.form.get("username")
        Password = request.form.get("password")
        Mobile = request.form.get("mobile")
        Email = request.form.get("email")
     #   print(username,password,mobile,email,"AAAAAAAAAAAAAAAAAAAAAAA")
        newusers = Users(username = Username, password = Password,mobile= Mobile, email = Email)
        Session.add(newusers)
        Session.commit()
        otp = random.randint(0000,9999)
        POOL.set(Mobile, otp)
        print(POOL,'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP')
        message = client.messages \
                .create(
                    #  body=" AXIS BANK INR 20000.00 Debited from A/c no. XX098765 31-10-2022 17:36:50 ATM_WDL/AXIS BANK SMS BLOCKCARD 0048 to +918691000002, if not done by you- contact   ",
                    body="Otp is :"+str(otp),
                    from_='+19702870724',
                    to= "+91"+Mobile 
                )

        print(message.sid)
        # return render_template('register.html')
        return render_template('otp.html', result = Mobile)


@app.route('/otp', methods =['POST'])
def otp_verification():
    getotp = POOL.get(request.form.get("mobile"))
    aaa = getotp.decode("UTF-8")
    bbb = ast.literal_eval(aaa)
    if str(bbb) == request.form.get("otp"):
        return render_template('index.html')
    else:
        return "Otp Entered Wrong" 
    


@app.route('/email', methods =['POST'])
def email_send():
    email = request.form.get("to_email")
    Message = request.form.get("message")
    import smtplib
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("sahil.chettiar@routemobile.com", "qqzqhdqjskzzfgaw")
    message = Message
    s.sendmail("sahil.chettiar@routemobile.com", email, message)
    s.quit()
    return render_template('index.html') 

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)

