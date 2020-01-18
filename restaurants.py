import tkinter as tk
import json
import startmenu

with open("restaurants.json") as f: restaurantData = json.load(f)
order = []

def numberOrdered(restaurant, menuType, itemId):
  num = 0
  for i in order:
    if i.restaurant == restaurant and i.menuType == menuType and i.itemId == itemId: num += 1
  return num

class OrderItem:
  def __init__(self, restaurant, menuType, itemId):
    self.restaurant = restaurant
    self.menuType = menuType
    self.itemId = itemId
  def getItem(self):
    for i in restaurantData["restaurants"]:
      if i["name"] != self.restaurant: continue
      for j in i["menus"]:
        if j["type"] != self.menuType: continue
        for k in j["selections"]:
          if k["id"] == self.itemId: return k

class RestaurantButton(tk.Frame):
  def __init__(self, parent=None, name="", displayName=None, extraLabel=0):
    super().__init__(parent)
    self.parent = parent
    self.pack()
    self.clicked = 0
    self.button = tk.Button(self, text=(displayName if displayName else name), command=self.wasClicked)
    self.button.pack(side="left")
    self.name = name
    self.extraLabel = extraLabel
    if extraLabel:
      self.labelValue = tk.StringVar()
      self.label = tk.Label(self, textvariable=self.labelValue)
      self.label.pack(side="right")
  def wasClicked(self): self.clicked = 1
  def isClicked(self):
    if self.clicked:
      self.clicked = 0
      return 1
    return 0
  def setLabel(self, text): self.labelValue.set(text)
  def getName(self): return self.name
  def destroy(self):
    self.button.destroy()
    if self.extraLabel: self.label.destroy()
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
    self.ordering = 0
    for i in order:
      if i.restaurant == self.name:
        self.ordering = 1
        break
    self.makeWidgets()
  def makeWidgets(self):
    self.title = tk.Label(self, text=self.name, font=("Helvetica", 36))
    self.title.pack()
    self.menus = []
    for i in self.restaurantData["menus"]:
      self.menus.append(RestaurantButton(self, i["type"], restaurantData["typeNames"][i["type"]]))
      self.menus[-1].pack()
    self.backButton = tk.Button(self, text="Place Order" if self.ordering else "Go Back", command=self.backClicked)
    self.backButton.pack()
  def update(self):
    if self.back: return RestaurantMenu(self.parent, self.name) if self.ordering else startmenu.Start(self.parent)
    for i in self.menus:
      if i.isClicked(): return RestaurantItemMenu(self.parent, self.name, i.getName())
  def backClicked(self):
    global order
    self.back = 1
    if self.ordering: order = []
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
      self.items.append(RestaurantButton(self, str(i["id"]), i["name"], 1))
      self.items[-1].setLabel("Ordered: %i" % numberOrdered(self.name, self.mealType, i["id"]))
      self.items[-1].pack()
    self.backButton = tk.Button(self, text="Go Back", command=self.backClicked)
    self.backButton.pack()
  def update(self):
    if self.back: return RestaurantMenu(self.parent, self.name)
    for i in self.items:
      if i.isClicked():
        order.append(OrderItem(self.name, self.mealType, int(i.getName())))
        i.setLabel("Ordered: %i" % numberOrdered(self.name, self.mealType, int(i.getName())))
    
  def backClicked(self): self.back = 1
  def destroy(self):
    self.title.destroy()
    for i in self.items: i.destroy()
    self.backButton.destroy()
    super().destroy()
    