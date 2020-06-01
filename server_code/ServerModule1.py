import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from datetime import datetime, timedelta
from gpiozero import pi_info, CPUTemperature
import pyjokes

pi = pi_info()
cpu = CPUTemperature()

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def get_model():
  return pi.model

@anvil.server.callable
def get_revision_code():
  return pi.revision

@anvil.server.callable
def get_hostname():
  with open('/etc/hostname') as f:
    return f.readline()

@anvil.server.callable
def get_temperature():
  return cpu.temperature

@anvil.server.callable
def get_joke():
  return pyjokes.get_joke()

def delete_old_temperatures():
  yesterday = datetime.now() - timedelta(days=1)
  old_temps = app_tables.temperatures.search(
    datetime=q.less_than(yesterday)
  )
  for row in old_temps:
    row.delete()

@anvil.server.background_task
def save_temperature():
  delete_old_temperatures()
  app_tables.temperatures.add_row(
    datetime=datetime.now(),
    temperature=cpu.temperature,
  )

@anvil.server.callable
def get_temperature_data():
  data = app_tables.temperatures.search()
  dts = [str(d['datetime']) for d in data]
  temps = [d['temperature'] for d in data]
  return (dts, temps)
