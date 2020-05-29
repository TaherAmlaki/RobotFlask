class RobotListenerExecution:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.tests = {}
        self._current_test_keywords = []
        self._current_test = None
        self._current_suite = None
        self.queue = None
        self._level = 0

    def start_suite(self, name, attributes):
        self._current_suite = name
        self.queue.put(self.tests)

    def start_test(self, name, attributes):
        self._level = 1
        self._current_test_keywords = []
        self._current_test = name
        self.tests[(self._current_suite, self._current_test)] = {"keywords": [], "status": "running"}
        self.queue.put(self.tests)

    def start_keyword(self, name, attributes):
        if self._level < 2:
            self._current_test_keywords.append(attributes.get("kwname", name.split(".")[-1]))
            self.tests[(self._current_suite, self._current_test)]["keywords"] = self._current_test_keywords.copy()
            self.queue.put(self.tests)
        self._level += 1

    def end_keyword(self, name, attributes):
        self._level -= 1

    def log_message(self, message):
        if self._level < 2:
            self._current_test_keywords.append('log')
            self.tests[(self._current_suite, self._current_test)]["keywords"] = self._current_test_keywords.copy()
            self.queue.put(self.tests)

    def end_test(self, name, attributes):
        self.tests[(self._current_suite, self._current_test)] = {"keywords": self._current_test_keywords, "status": attributes.get("status", "pass")}
        self.queue.put(self.tests)
        self._level = 0
        self._current_test = None
        self._current_test_keywords = []

    def end_suite(self, name, attributes):
        self._current_suite = None
