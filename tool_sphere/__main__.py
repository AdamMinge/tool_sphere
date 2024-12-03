import sys
import logging

from tool_sphere import Application, MainWindow

_formatter = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
_handler_with_formatter = logging.StreamHandler(stream=sys.stdout)
_handler_with_formatter.setFormatter(_formatter)
logging.basicConfig(handlers=[_handler_with_formatter])


def main():
    app = Application(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
