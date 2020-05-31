import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from datetime import datetime

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def get_model():
  return "Some model number"

@anvil.server.callable
def get_revision_code():
  return "Some rev code"

@anvil.server.callable
def get_hostname():
  return "Some hostname"

@anvil.server.callable
def get_temperature():
  return "Some temperature"

@anvil.server.callable
def get_joke():
  return "Some joke"

@anvil.server.callable
def save_temperature():
  app_tables.temperatures.add_row(
    datetime=datetime.now(),
    temperature=53,
  )
  
@anvil.server.callable
def get_temperature_data():
  data = app_tables.temperatures.search()
  dts = [str(d['datetime']) for d in data]
  temps = [d['temperature'] for d in data]
  return (dts, temps)