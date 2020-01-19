import tkinter as tk
from restaurants import RestaurantList, RestaurantMenu

class Start(tk.Frame):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.parent = parent
    self.pack()
    self.makeWidgets()
  def makeWidgets(self):
    self.title = tk.Label(self, text="Get In My Belly", font=("Helvetica", 48))
    self.title.pack()
    self.restaurants = RestaurantList(self)
    self.restaurants.pack()
  def update(self):
    selection = self.restaurants.getSelection()
    if selection != None:
      return RestaurantMenu(self.parent, selection)
    return None
  def destroy(self):
    self.title.destroy()
    self.restaurants.destroy()
    super().destroy()