

class Node():
    def __init__(self):
        self.tag = ""
        self.connected_to =

def read_nodes():
   # self.start_y = test.half_reserved_height
   # self.start_x = test.half_reserved_width


    with open("text files/Nodes.txt", 'r') as node_file:
        file_context = node_file.readlines()
        for line in file_context:
            for char in line:
                if char == "A":




read_nodes()