from core import Geoffrey
from pathlib import Path


# basic pre-running setup
# not implemented yet
def run():
    bot = Geoffrey(root_dir=Path(__file__).parent)
    bot.run()


if __name__ == "__main__":
    run()
