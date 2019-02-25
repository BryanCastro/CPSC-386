import pygame


class High_Scores:

    def __init__(self):
        #self.high_scores = []
        #self.initials = []
        #self.num_of_high_scores = len(self.high_scores)

        #with open(r"txt_files/high_scores.txt", "r+") as f:
        #    data = f.readlines()
        #    print(data)
        #    for line in data:
        #        self.high_scores.append(line.strip().split(",")[1])
        #        # strip to remove the \n
        #        # split at every interval of comma
        #        # second element is indexed 1
        #        self.initials.append(line.strip().split(",")[0])

        self.score_list = []
        #self.update_scores()


    def update_scores(self):

        self.score_list.clear()

        with open(r"txt_files/high_scores.txt", "r+") as f:
            data = f.readlines()
            for line in data:
                self.score_list.append(int(line.strip("\n")))

        self.score_list.sort(reverse = True)

    def add_score(self, score):
        with open("txt_files/high_scores.txt", "a") as myFile:
            myFile.write("\n" + score)
            myFile.close()

