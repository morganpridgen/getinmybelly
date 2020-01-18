import tkinter as tk
from startmenu import Start

class GetInMyBelly(tk.Frame):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.parent = parent
    self.pack()
    self.makeWidgets()
    self.onUpdate()
  def makeWidgets(self):
    self.state = Start(parent=self)
    self.state.pack()
  def onUpdate(self):
    newState = self.state.update()
    if newState:
      self.state.destroy()
      self.state = newState
    self.after(100, self.onUpdate)

if __name__ == "__main__":
  root = tk.Tk()
  app = GetInMyBelly(parent=root)
  app.mainloop()