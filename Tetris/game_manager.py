class GameManager:
    __instance = None

    @staticmethod
    def get_instance():
        if GameManager.__instance is None:
            GameManager()
        return GameManager.__instance

    def __init__(self):
        self.check_instance()
        self.best = 0
        self.score = 0
        self.lines = 0
        self.state = "menu"
        self.show_help = False

    def check_instance(self):
        if GameManager.__instance is not None:
            raise Exception("This is a singleton class. Cannot be instantiated.")
        else:
            GameManager.__instance = self 