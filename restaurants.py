import tkinter as tk
import json
import startmenu

with open("restaurants.json") as f: restaurantData = json.load(f)

class RestaurantButton(tk.Frame):
  def __init__(self, parent=None, name="", displayName=None):
    super().__init__(parent)
    self.parent = parent
    self.pack()
    self.clicked = 0
    self.button = tk.Button(self, text=(displayName if displayName else name), command=self.wasClicked)
    self.button.pack()
    self.name = name
  def wasClicked(self): self.clicked = 1
  def isClicked(self): return self.clicked
  def getName(self): return self.name
  def destroy(self):
    self.button.destroy()
    super().destroy()

class RestaurantList(tk.Frame):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.parent = parent
    self.pack()
    self.makeWidgets()
  def makeWidgets(self):
    self.restaurants = []
    for i in restaurantData["restaurants"]:
      self.restaurants.append(RestaurantButton(self, i["name"]))
      self.restaurants[-1].pack()
  def getSelection(self):
    for i in self.restaurants:
      if i.isClicked(): return i.getName()
    return None
  def destroy(self):
    for i in self.restaurants: i.destroy()
    super().destroy()

class RestaurantMenu(tk.Frame):
  def __init__(self, parent=None, name=""):
    super().__init__(parent)
    self.parent = parent
    self.pack()
    self.back = 0
    for i in restaurantData["restaurants"]:
      if i["name"] == name:
        self.name = name
        self.restaurantData = i
        break
    self.makeWidgets()
  def makeWidgets(self):
    self.title = tk.Label(self, text=self.name, font=("Helvetica", 36))
    self.title.pack()
    self.menus = []
    for i in self.restaurantData["menus"]:
      self.menus.append(RestaurantButton(self, i["type"], restaurantData["typeNames"][i["type"]]))
      self.menus[-1].pack()
    self.backButton = tk.Button(self, text="Go Back", command=self.backClicked)
    self.backButton.pack()
  def update(self):
    if self.back: return startmenu.Start(self.parent)
    for i in self.menus:
      if i.isClicked(): return RestaurantItemMenu(self.parent, self.name, i.getName())
  def backClicked(self): self.back = 1
  def destroy(self):
    self.title.destroy()
    for i in self.menus: i.destroy()
    self.backButton.destroy()
    super().destroy()

class RestaurantItemMenu(tk.Frame):
  def __init__(self, parent=None, name="", mealType=""):
    super().__init__(parent)
    self.parent = parent
    self.pack()
    self.back = 0
    for i in restaurantData["restaurants"]:
      if i["name"] == name:
        self.name = name
        self.restaurantData = i
        break
    for i in self.restaurantData["menus"]:
      if i["type"] == mealType:
        self.mealType = mealType
        self.mealData = i
        break
    self.makeWidgets()
  def makeWidgets(self):
    self.title = tk.Label(self, text="%s: %s" % (self.name, restaurantData["typeNames"][self.mealType]), font=("Helvetica", 36))
    self.title.pack()
    self.items = []
    for i in self.mealData["selections"]:
      self.items.append(RestaurantButton(self, str(i["id"]), i["name"]))
      self.items[-1].pack()
    self.backButton = tk.Button(self, text="Go Back", command=self.backClicked)
    self.backButton.pack()
  def update(self):
    if self.back: return RestaurantMenu(self.parent, self.name)
  def backClicked(self): self.back = 1
  def destroy(self):
    self.title.destroy()
    for i in self.items: i.destroy()
    self.backButton.destroy()
    super().destroy()
    