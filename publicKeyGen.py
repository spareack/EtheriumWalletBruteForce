
import wx


class MainFrame(wx.Frame): 
    def __init__(self):
        wx.Frame.__init__(self, None, title="Minimize to Tray")
        panel = wx.Panel(self)
 
        self.Bind(wx.EVT_ICONIZE, self.onMinimize)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Show()
 
    def onClose(self, evt):
        self.Destroy()
 
    def onMinimize(self, event):
        if self.IsIconized():
            self.Hide()
 

def main():
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
 
if __name__ == "__main__":
    main()

