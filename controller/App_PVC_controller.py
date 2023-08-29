import sys

class AppPVCController :
    def onOpen(self) :
        print("onOpen")

    def onSave(self) :
        print("onSave")

    def onSaveAs(self): 
        print("onSaveAs")

    def onExit(self):
        sys.exit()