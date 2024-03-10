class Bar:
    fill_letter = "║"#"▏"#" ▎"#  #

    elements = {
        "begin": {
            "upper": "┏",
            "progress": " ",
            "lower": "┗"
        },
        "middle": {
            "upper": "━",
            "progress": fill_letter,
            "lower": "━"
        },
        "middle_filled": {
            "upper": "━",
            "progress": "█",
            "lower": "━"
        },
        "end": {
            "upper": "┓",
            "progress": " ",
            "lower": "┛"
        }
    }

    progress_letter = "█"
    start_letter = " ▎" # test char ▏
    #"║" is working on win and linux
    # "⎹" works only windows


    def __init__(self, max_progress=25, progress=20, max_charlength=30):
        self.maxProgress = max_progress
        self.progress = progress
        self.char_length = max_charlength

        if progress > max_progress:
            progress = max_progress

        bar = {
            "begin": self.elements["begin"],
            "middle": [],
            "end": self.elements["end"],
        }

        div = max_charlength/max_progress
        filled_length = int(div*progress)

        for i in range(filled_length):
            bar["middle"].append(self.elements["middle_filled"])

        for i in range(max_charlength-filled_length):
            bar["middle"].append(self.elements["middle"])

        self.bar = bar

    def get_bar(self):
        bar_str = ""

        # upper part
        bar_str += self.bar["begin"]["upper"]
        for i in self.bar["middle"]:
            bar_str += i["upper"]
        bar_str += self.bar["end"]["upper"] + "\n"

        #middle part
        bar_str += " " #+ self.start_letter
        for i in self.bar["middle"]:
            bar_str += i["progress"]
        bar_str += " \n" #self.start_letter + " \n"

        #bottom part
        bar_str += self.bar["begin"]["lower"]
        for i in self.bar["middle"]:
            bar_str += i["lower"]
        bar_str += self.bar["end"]["lower"]

        return bar_str

    def getBar_old(self, progress=None):
        bar = ""
        if progress: self.progress = progress

        if self.progress <= self.maxProgress:
            bar = self.upper + "\n" + " "
            for p in range(self.progress):
                bar += self.progress_letter
            for missing in range(self.maxProgress - self.progress):
                bar += self.fill_letter
            bar += "\n" + self.lower
        else:
            bar = self.upper + "\n" + " "
            for p in range(self.maxProgress):
                bar += self.progress_letter
            bar += "\n" + self.lower + "\n Bonus: " + str(self.progress - self.maxProgress)

        return bar

    def addProgress(self, value):
        self.progress += int(value)

if __name__ == "__main__":
    bar = Bar(400, 180, 25)
    print(bar.get_bar())
