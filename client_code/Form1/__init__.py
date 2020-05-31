from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import plotly.graph_objects as go

class Form1(Form1Template):

  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.model.text = anvil.server.call('get_model')
    self.revision.text = anvil.server.call('get_revision_code')
    self.hostname.text = anvil.server.call('get_hostname')
    self.temperature.text = anvil.server.call('get_temperature')
    anvil.server.call('save_temperature')
    
    dts, temperatures = anvil.server.call('get_temperature_data')
    
    temp = go.Scatter(
      x=dts,
      y=temperatures,
      name="CPU Temperature",
    )
    
    self.temperature_plot.data = [temp]
    
  def get_joke(self, **event_args):
    joke = anvil.server.call('get_joke')
    alert(joke)



