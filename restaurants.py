import tkinter as tk
import json
import startmenu

with open("restaurants.json") as f: restaurantData = json.load(f)
order = []

def numberOrdered(restaurantId, typeId, itemId):
  num = 0
  for i in order:
    if i.restaurantId == restaurantId and i.typeId == typeId and i.itemId == itemId: num += 1
  return num

def orderCost():
  cost = 0
  for i in order: cost += i.getItem()["cost"]
  return cost

class OrderItem:
  def __init__(self, restaurantId, typeId, itemId):
    self.restaurantId = restaurantId
    self.typeId = typeId
    self.itemId = itemId
  
  def getItem(self):
    for i in restaurantData["restaurants"]:
      if i["id"] != self.restaurantId: continue
      for j in i["menus"]:
        if j["id"] != self.typeId: continue
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
      self.restaurants.append(RestaurantButton(self, i["id"], i["name"]))
      self.restaurants[-1].pack()
  
  def getSelection(self):
    for i in self.restaurants:
      if i.isClicked(): return i.getName()
    return None
  
  def destroy(self):
    for i in self.restaurants: i.destroy()
    super().destroy()

class RestaurantMenu(tk.Frame):
  def __init__(self, parent=None, restaurantId=""):
    super().__init__(parent)
    self.parent = parent
    self.pack()
    self.back = 0
    self.show = 0
    for i in restaurantData["restaurants"]:
      if i["id"] == restaurantId:
        self.restaurantId = restaurantId
        self.restaurantData = i
        break
    self.ordering = 0
    for i in order:
      if i.restaurantId == self.restaurantId:
        self.ordering = 1
        break
    self.makeWidgets()
  
  def makeWidgets(self):
    self.title = tk.Label(self, text=self.restaurantData["name"], font=("Helvetica", 36))
    self.title.pack()
    self.menus = []
    for i in self.restaurantData["menus"]:
      self.menus.append(RestaurantButton(self, i["id"], i["type"]))
      self.menus[-1].pack()
    self.backButton = tk.Button(self, text="Place Order" if self.ordering else "Go Back", command=self.backClicked)
    self.backButton.pack()
    self.costLabel = tk.Label(self, text="Cost: $%.2f" % orderCost())
    self.costLabel.pack()
    self.viewFood = tk.Button(self, text="Show me the food", command=self.showClicked)
    self.viewFood.pack()
  
  def update(self):
    if self.back: return RestaurantMenu(self.parent, self.restaurantId) if self.ordering else startmenu.Start(self.parent)
    if self.show: return OrderView(self.parent, self.restaurantId)
    for i in self.menus:
      if i.isClicked(): return RestaurantItemMenu(self.parent, self.restaurantId, i.getName())
  
  def backClicked(self):
    global order
    self.back = 1
    if self.ordering: order = []
  
  def showClicked(self): self.show = 1
  
  def destroy(self):
    self.title.destroy()
    for i in self.menus: i.destroy()
    self.backButton.destroy()
    super().destroy()

class RestaurantItemMenu(tk.Frame):
  def __init__(self, parent=None, restaurantId="", typeId=""):
    super().__init__(parent)
    self.parent = parent
    self.pack()
    self.back = 0
    for i in restaurantData["restaurants"]:
      if i["id"] == restaurantId:
        self.restaurantId = restaurantId
        self.restaurantData = i
        break
    for i in self.restaurantData["menus"]:
      if i["id"] == typeId:
        self.typeId = typeId
        self.typeData = i
        break
    self.makeWidgets()
  
  def makeWidgets(self):
    self.title = tk.Label(self, text="%s: %s" % (self.restaurantData["name"], self.typeData["type"]), font=("Helvetica", 36))
    self.title.pack()
    self.items = []
    for i in self.typeData["selections"]:
      self.items.append(RestaurantButton(self, str(i["id"]), "%s ($%.2f)" % (i["name"], i["cost"]), 1))
      self.items[-1].setLabel("Ordered: %i" % numberOrdered(self.restaurantId, self.typeId, i["id"]))
      self.items[-1].pack()
    self.backButton = tk.Button(self, text="Go Back", command=self.backClicked)
    self.backButton.pack()
    self.foodImage = tk.PhotoImage(file="images/%i/%i/0.gif" % (self.restaurantId, self.typeId))
    self.foodImageLabel = tk.Label(self, image=self.foodImage)
    self.foodImageLabel.pack()
  
  def update(self):
    if self.back: return RestaurantMenu(self.parent, self.restaurantId)
    for i in self.items:
      if i.isClicked():
        order.append(OrderItem(self.restaurantId, self.typeId, int(i.getName())))
        i.setLabel("Ordered: %i" % numberOrdered(self.restaurantId, self.typeId, int(i.getName())))
  
  def backClicked(self): self.back = 1
  
  def destroy(self):
    self.title.destroy()
    for i in self.items: i.destroy()
    self.backButton.destroy()
    self.foodImageLabel.destroy()
    super().destroy()

class OrderIcon(tk.Frame):
  def __init__(self, parent=None, item=None):
    super().__init__(parent)
    self.parent = parent
    self.pack()
    self.item = item
    self.makeWidgets()
  
  def makeWidgets(self):
    self.image = tk.PhotoImage(file="images/%i/%i/%i.gif" % (self.item.restaurantId, self.item.typeId, self.item.itemId))
    self.imageLabel = tk.Label(self, image=self.image)
    self.imageLabel.pack(side="left")
    self.nameLabel = tk.Label(self, text="%s (%.2f)" % (self.item.getItem()["name"], self.item.getItem()["cost"]))
    self.nameLabel.pack()
  
  def destroy(self):
    self.imageLabel.destroy()
    self.nameLabel.destroy()
    super().destroy()

class OrderIconRow(tk.Frame):
  def __init__(self, parent=None, items=[]):
    super().__init__(parent)
    self.parent = parent
    self.pack()
    self.items = items
    for i in self.items: i.pack(side="left")
  
  def destroy(self):
    for i in self.items: i.destroy()
    super().destroy()

class OrderView(tk.Frame):
  def __init__(self, parent=None, restaurantId=""):
    super().__init__(parent)
    self.parent = parent
    self.pack()
    self.back = 0
    for i in restaurantData["restaurants"]:
      if i["id"] == restaurantId:
        self.restaurantId = restaurantId
        self.restaurantData = i
        break
    self.makeWidgets()
  
  def makeWidgets(self):
    self.title = tk.Label(self, text="%s: Order" % self.restaurantData["name"], font=("Helvetica", 36))
    self.title.pack()
    self.icons = []
    rowIcons = []
    for i in order:
      rowIcons.append(OrderIcon(self, i))
      if len(rowIcons) == 4:
        self.icons.append(OrderIconRow(self, rowIcons[:]))
        self.icons[-1].pack(side="top")
        rowIcons = []
    if len(rowIcons) > 0:
      self.icons.append(OrderIconRow(self, rowIcons[:]))
      self.icons[-1].pack(side="top")
    self.backButton = tk.Button(self, text="Go Back", command=self.backClicked)
    self.backButton.pack()
  
  def update(self):
    if self.back: return RestaurantMenu(self.parent, self.restaurantId)
  
  def backClicked(self): self.back = 1
  
  def destroy(self):
    self.title.destroy()
    for i in self.icons: i.destroy()
    self.backButton.destroy()
    super().destroy()