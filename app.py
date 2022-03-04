from flask import Flask, render_template, request, redirect, session
import random
import datetime

app = Flask(__name__)
app.secret_key = 'claveSecreta'

@app.route('/')
def index():
    if 'actividad' in session:
        return render_template("index.html", students = session["actividad"], money = session["money"], show = session["changes"],
        oportunidades = session["oportunidades"], message=session["mensaje"])
    else:
        session["actividad"] = []
        session["money"] = 0
        session["oportunidades"] = 15
        session["changes"] = False
        session["mensaje"] = ""
        return render_template("index.html", students = session["actividad"], money = session["money"], show = session["changes"], 
        oportunidades= session["oportunidades"], message=session["mensaje"])

@app.route('/process_money',methods=['POST'])
def process_momey():
    fechaHora = datetime.datetime.now()
    auxMoney = int(session["money"])
    numerosRandon = [random.randint(10,20),random.randint(5,10),random.randint(2,5),random.randint(0,50)]
    valores = ['farm','cave','house', 'casino']
    Activi = []
    auxActivi = []

    if(request.form['lugar']==valores[0]):
        session["numero"] = numerosRandon[0]
        session["estado"] = 1
        auxMoney += numerosRandon[0]
    elif (request.form['lugar']==valores[1]):
        session["numero"] = numerosRandon[1]
        session["estado"] = 1
        auxMoney += numerosRandon[1]
    elif (request.form['lugar']==valores[2]):
        session["numero"] = numerosRandon[2]
        session["estado"] = 1
        auxMoney += numerosRandon[2]
    else:
        session["numero"] = numerosRandon[3]
        session["estado"] = random.randint(1,2)
        if(int(session["estado"])==1):
            auxMoney += numerosRandon[3]
        else:
            auxMoney -= numerosRandon[3]
    
    session["money"] = auxMoney

    if 'actividad' in session:
        for i in session["actividad"]:
            auxActivi.append(i)
        activi = {'numero': session["numero"], 'estado': session["estado"], 'lugar': request.form['lugar'], 'fh':fechaHora.strftime('%Y/%m/%d %I:%M %p') }
        auxActivi.append(activi)
        session["actividad"] = auxActivi
    else:
        activi = {'numero': session["numero"], 'estado': session["estado"], 'lugar': request.form['lugar'], 'fh':fechaHora.strftime('%Y/%m/%d %I:%M %p') }
        Activi.append(activi)
        session["actividad"] = Activi
    
    if 'oportunidades' in session:
        session["oportunidades"] -= 1
        opt = int(session["oportunidades"])
    
    if(auxMoney>=500):
        session["changes"] = True
        session["mensaje"] = "<h2>Ganastes!</h2>"
    else:
        if(opt==0):
            session["changes"] = True
            session["mensaje"] = "<h2>Perdiste!</h2>"
    return redirect("/")

@app.route('/reset')
def reset():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)