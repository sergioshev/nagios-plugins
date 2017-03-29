#!/usr/bin/python

from  zkemapi import zkem
import datetime
import getopt
import math
import pprint
from exceptions import StandardError
import sys


#
# -h el nombre del host (del fichero) o ip
# -w limite de desvio en segundos para el warning
# -c limite de desvio en segundos para el critical
#
# return values
# UNKNOWN = 3
# CRITICAL = 2
# WARNING = 1
# OK = 0

#codigos de salida
UNKNOWN = 3
CRITICAL = 2
WARNING = 1
OK = 0

# ofsets
warn_offset, crit_offset = (0,0)
host = ''

#intervalos en segundos
SMIN = 60
SHOUR = SMIN * 60
SDAY = SHOUR * 24

# devuelve true o false
# si 'ts' se desvia del 'ref_ts' retorna la cantidad de sgundos
def delta_seconds(ts, ref_ts = None):
  if (not ref_ts):
    ref_ts = datetime.datetime.now()
#  print "REF_TS:" + ref_ts.strftime('%Y-%m-%d %H:%M:%S')
#  print "TS    :" + ts.strftime('%Y-%m-%d %H:%M:%S')
  delta = ts - ref_ts
#  print "delta days:" + str(delta.days) + " delta seconds:" + str(delta.seconds)
  ts_delta = int(delta.days*SDAY+delta.seconds)
  return ts_delta

params, extra_args = getopt.getopt(sys.argv[1:], 'h:w:c:')
for (param,param_value) in params:
  if (param == "-w"):
    warn_offset = param_value
  if (param == "-c"):
    crit_offset = param_value
  if (param == "-h"):
    host = param_value

if (not warn_offset or warn_offset <= 0 or \
    not crit_offset or crit_offset <= 0 or \
    not host):
  print "Use: -h host | ip addr -w warn_offset (sec) -c crit_offset (sec)"
  sys.exit(UNKNOWN)

if ( not warn_offset.isdigit() or not crit_offset.isdigit() ):
  print "ERROR: wrong limits for -w or -c"
  sys.exit(UNKNOWN)


crit_offset, warn_offset = (int(crit_offset), int(warn_offset))
if (crit_offset < warn_offset):
  aux = crit_offset
  crit_offset = warn_offset
  warn_offset = aux

ac_dev=zkem()
status_cx = ac_dev.connect(host = host, debug = False, timeout = 7)
if status_cx:
  ts = ac_dev.get_time()
  ac_dev.disconnect()
  ts = datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
  ts_str = ts.strftime('%Y-%m-%d %H:%M:%S')
  delta = delta_seconds(ts);
  # delta puede ser negativo si la fecha de referencia esta en 
  # el pasado con respecto a la chequeada, por eso uso valor
  # absoluto
  delta_abs = int(math.fabs(delta))
 
  if (delta_abs > crit_offset):
    print "CRITICAL: ts_fichador=" + ts_str + " delta=" + str(delta) + "  warn=" + str(warn_offset) + "  crit=" + str(crit_offset)
    sys.exit(CRITICAL)

  if (delta_abs >= warn_offset and delta_abs < crit_offset ):
    print "WARNING: ts_fichador=" + ts_str + " delta=" + str(delta) + "  warn=" + str(warn_offset) + "  crit=" + str(crit_offset)
    sys.exit(WARNING)

  if (delta_abs < warn_offset):
    print "OK: ts_fichador=" + ts_str + " delta=" + str(delta) + "  warn=" + str(warn_offset) + "  crit=" + str(crit_offset)
    sys.exit(OK)

else:
  print "ERROR: Can't connecto to " + host
  sys.exit(UNKNOWN)
