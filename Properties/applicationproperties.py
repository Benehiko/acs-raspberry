

class AppProperties:

    def __init__(self, no_network=False, save_drawn=False, show_drawn=False, always_save=False, camera_preview=False, capture_limit=None, post_url=None):

        self.no_network = no_network
        self.show_drawn = show_drawn
        self.always_save = always_save
        self.camera_preview = camera_preview
        self.post_url = post_url
        self.capture_limit = capture_limit
        self.save_drawn = save_drawn

    def network_status(self):
        return self.no_network

    def set_network_status(self, no_network=False):
        self.no_network = no_network

    def get_show_drawn(self):
        return self.show_drawn

    def set_show_drawn(self, show_drawn=False):
        self.show_drawn = show_drawn

    def get_always_save(self):
        return self.always_save

    def set_always_save(self, always_save=False):
        self.always_save = always_save

    def get_camera_preview(self):
        return self.camera_preview

    def set_camera_preview(self, camera_preview=False):
        self.camera_preview = camera_preview

    def get_post_url(self):
        return self.post_url

    def set_post_url(self, post_url=None):
        self.post_url = post_url

    def get_capture_limit(self):
        return self.capture_limit

    def set_capture_limit(self, capture_limit=None):
        self.capture_limit = capture_limit

    def get_save_drawn(self):
        return self.save_drawn

    def set_save_drawn(self, save_drawn=False):
        self.save_drawn = save_drawn