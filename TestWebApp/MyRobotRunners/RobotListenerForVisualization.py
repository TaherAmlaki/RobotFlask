class RobotListenerForVisualization:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, level=5):
        self._level = level
        self._current_level = 0
        self.links = []
        self._link = []

    def start_suite(self, name, attributes):
        pass

    def start_test(self, name, attributes):
        self._current_level = 0
        self._link = [name]

    def start_keyword(self, name, attributes):
        self._current_level += 1
        if self._current_level < self._level:
            self._link.append(attributes.get("kwname"))

    def end_keyword(self, name, attributes):
        if self._current_level < self._level:
            self.links.append(self._link.copy())
            self._link.pop()
        self._current_level -= 1

    def end_test(self, name, attributes):
        self.links.append(self._link.copy())
        self._link.pop()

    def end_suite(self, name, attributes):
        pass

    def log_message(self, message):
        pass

    def close(self):
        pass
