class DashboardView:
    def __init__(self, view_model):
        self.view_model = view_model

    def display_projects(self):
        return self.view_model.projects

    def display_timer(self):
        return self.view_model.get_elapsed_time()
