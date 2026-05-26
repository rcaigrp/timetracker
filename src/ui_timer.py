class TimerView:
    def __init__(self, view_model):
        self.view_model = view_model

    def start(self):
        self.view_model.start_timer()

    def pause(self):
        self.view_model.pause_timer()

    def stop(self):
        self.view_model.stop_timer()

    def get_elapsed_time(self):
        return self.view_model.get_elapsed_time()
