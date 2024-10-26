import requests, os, signal, json, sys # For capabilites
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, g # Web interface
app = Flask(__name__) # Define FLASK APP NAME
def signal_handler(): # Ctrl C handler
    print("[i] Saliendo del programa..")
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler) # Ctrl C shooter

def makeReservation(date): # https://atcsports.io/checkout/518?day={date}&court={1568(n) + 1 }&sport_id=2 (2 = Futbol)&duration={durationMinutes}&start={startTime}%3A{30 o 00 minutos}&end=&is_beelup=false
    durationMinutes = "30" # Duracion de la cancha en minutos
    date = date # Fecha dada por timeAndShoot
    court = int(1568) # Numero de operacion
    sport_id = int(2) # Sport id - 2 = Futbol
    startTime = "9"  # startTime - Viernes 
    minuteShooter = "30"
     #  https://atcsports.io/checkout/518?day=2024-11-01&court=1569&sport_id=2&duration=60&start=13%3A00&end=&is_beelup=false
    url = "https://www.facebook.com/tr/"
    dl = f"https://atcsports.io/checkout/518?day={date}&court={court}&sport_id={sport_id}&duration={durationMinutes}&start={startTime}%3A{minuteShooter}&end=&is_beelup=false"
    print(f"[I] URL to atcsports.io: {dl}")
    data = {
        "id": "730149647599243",
        "ev": "SubscribedButtonClick",
        "dl": f"{dl}",
        "rl": "",
        "if": "false",
        "ts": "1729959637398", # changeW
        "cd[buttonFeatures]": '{"classList":"min-w-[10rem] py-2 px-5 text-sm font-semibold transition-colors inline-block cursor-pointer\n                            rounded-3xl \n                            bg-primary-p1 text-misc-white hover:bg-primary-p2\n                            false\n                            false \n                            false\n                            false\n                            false\n                            false\n                            \n                            w-1/2","destination":"","id":"","imageUrl":"","innerText":"Confirmar reserva","numChildButtons":0,"tag":"button","type":null,"name":"","value":""}',
        "cd[buttonText]": "Confirmar reserva",
        "cd[formFeatures]": "[]",
        "cd[pageFeatures]": '{"title":"Reserva tu cancha de padel o fútbol en todo LATAM - ATC"}',
        "cd[parameters]": "[]",
        "sw": "1600",
        "sh": "900",
        "udff[ph]": "91cea4a3fb805f89d2444a6c156013814c2d9e6724faeccacc80a097d045973a",
        "udff[em]": "e5a7f1388f332395691a0f853293c548721c61a81fb8ee9d1c274137131789ca",
        "v": "2.9.174",
        "r": "stable",
        "a": "tmgoogletagmanager",
        "ec": "3",
        "o": "6174",
        "fbp": "fb.1.1729959540430.618945909307486667",
        "cs_est": "true",
        "ler": "empty",
        "it": "1729959540026", # change
        "coo": "false",
        "es": "automatic",
        "tm": "3",
        "exp": "i2",
        "rqm": "SB",
    }
    optionsUrl = 'https://alquilatucancha.com/api/v2/bookings'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
        'Accept': '*/*',
        'Accept-Language': 'es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'authorization,content-type',
        'Referer': 'https://atcsports.io/',
        'Origin': 'https://atcsports.io',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Priority': 'u=4',
        'Te': 'trailers',
    }
    optionsResponse = requests.options(optionsUrl, headers=headers)
    response = requests.post(url, data=data)
    if response.status_code == 200 and optionsResponse.status_code == 200:
        print(f"[i] POST REQUEST TO {url}: OK")
    elif response.status_code == 200 and optionsResponse.status_code != 200:
        print(f"[i] POST REQUEST TO {url}: OK. {optionsUrl}: BAD")
        print(f"[i] Response {optionsUrl}: {optionsResponse.text}")
    elif response.status_code != 200 and optionsResponse.status_code == 200:
        print(f"[i] POST REQUEST TO {url}: BAD. {optionsUrl}: OK")

def timeAndshoot(todayDate): # View next days and if correct (if it Viernes Jueves or Domingo shoot the requests to meke the reservations)
    if isinstance(todayDate, str):
        todayDate = datetime.strptime(todayDate, "%d/%m/%Y").date()

    print(f"[i] Date: {todayDate.strftime('%d/%m/%Y')}")
    
    if todayDate.weekday() in [3, 4, 5]:
        todayDateIn2W = todayDate + timedelta(weeks=1)
        dateList = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        dateMatch = dateList[todayDateIn2W.weekday()]
        print(f"[i] Date in 2 weeks: {todayDateIn2W.strftime('%d/%m/%Y')}, {dateMatch}")
        rvDateFormat = todayDateIn2W.strftime('%Y-%m-%d')
        makeReservation(rvDateFormat)


def main():  #Main function
    todayDate = datetime.now()
    timeAndshoot(todayDate.date())

if __name__ == "__main__":
    main()