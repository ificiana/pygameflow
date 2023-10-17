import pygameflow as pgf

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650


views = {}


class MyGame(pgf.View):
    """
    Main application class.
    """

    def __init__(self, window):
        super().__init__(window)

    def setup(self):
        self.background_color = "black"
        pgf.set_title("View 1")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == pgf.K_RETURN:
            views["2"].show()


class MyGame2(pgf.View):
    """
    Main application class.
    """

    def __init__(self, window):
        super().__init__(window)

    def setup(self):
        self.background_color = "red"
        pgf.set_title("View 2")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == pgf.K_RETURN:
            views["1"].show()


def main():
    """Main function"""
    window = pgf.window.open_window(
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        resizable=True,
    )
    views["1"] = MyGame(window)
    views["2"] = MyGame2(window)

    views["1"].run()


if __name__ == "__main__":
    main()
