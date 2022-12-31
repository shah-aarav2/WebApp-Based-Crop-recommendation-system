from flask import Flask, render_template, redirect, jsonify, request, url_for
import pickle
import sklearn
import datetime as dt
date_details = dt.datetime.now()
day = date_details.weekday()
import smtplib

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
crop_list=["apple","banana","blackgram","chickpea","coconut","coffee",
           "cotton","grapes","jute","kidneybeans","mango","mothbeans","mungbean",
           "muskmelon","orange","papaya","pigeonpeas","pomegranate","rice",
           "watermelon"]
days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY",
        "FRIDAY", "SATURDAY", "SUNDAY"]


@app.route("/")
def home():
    global day, days
    return render_template("index.html",time=days[day])


@app.route("/Recommand_crop.html",methods=['POST','GET'])
def Recommand_crop():
    global model,crop_list
    b=1
    crop=""
    nitrogen=""
    phosphorus=""
    potassium=""
    temperature=""
    humidity=""
    ph=""
    rainfall=""
    predict=[]
    if request.method=='POST':
        nitrogen = float(request.form['nitrogen'])
        phosphorus = float(request.form['phosphorus'])
        potassium = float(request.form['potassium'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        predict = model.predict([[nitrogen,phosphorus,potassium,temperature,humidity,ph,rainfall]])
        a=str(predict)
        for _ in a:
            if _ == "1":
                crop=crop_list[b-9]
            else:
                b+=1
    else:
        pass
    # for _ in predict:
    return render_template("Recommand_crop.html",nitrovalue=crop,nitrogen=nitrogen,
                           phosphorus=phosphorus,potassium=potassium,temperature=temperature,humidity=humidity,
                           ph=ph,rainfall=rainfall)


@app.route("/contact_us.html",methods=['POST','GET'])
def contact_us():
    my_email = "codewithmrpy@gmail.com"
    password = "eaflyqlwydcznrgt"
    recipient= ["ranitsarkar71@gmail.com"]
    if request.method=="POST":
        name = request.form['name']
        recipient2 = (request.form['email']).lower()
        message1 = request.form['message']
        recipient.append(recipient2)
        for mail in recipient:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                # message to be sent
                SUBJECT = f"Thanks for your feedback {name}"
                TEXT = message1
                message = 'subject: {}\n\n{}'.format(SUBJECT, TEXT)
                connection.sendmail(
                        from_addr=my_email,
                        to_addrs=mail,
                        msg=message)
    else:
        pass
    return render_template("contact_us.html")


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)