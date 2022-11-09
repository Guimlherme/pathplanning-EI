class Command:
    def get_name(self):
        return "Abstract Command"

    def execute(self):
        raise Exception('Abstract Command cannot be executed')
