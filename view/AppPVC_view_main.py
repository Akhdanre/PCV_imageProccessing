from view.AppPVC_view_ui import PVC_view


class AppPVCViewMain(object):
    def __init__(self, model, controller):
        super().__init__()
        self.model = model
        self.controller = controller
        self.view = PVC_view()

        self.view.actionOpen.triggered.connect(self.controller.onOpen)