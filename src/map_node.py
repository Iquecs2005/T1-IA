class map_node:
    coord: tuple[int, int]
    gx: int
    hx: int
    fx: int
    parent: map_node

    def __init__(self, coord: tuple[int, int], gx: int, hx: int):
        self.coord = coord
        self.gx = gx
        self.hx = hx
        self.fx = gx + hx
        self.parent = None

    # heap always put the new node after the previous open one
    def __lt__(self, other: map_node):
        return False

    def get_coord(self):
        return self.coord

    def get_gx(self):
        return self.gx

    def set_gx(self, value):
        self.gx = value

    def get_hx(self):
        return self.hx

    def get_fx(self):
        return self.fx

    def set_fx(self, value):
        self.fx = value

    def get_parent(self):
        return self.parent

    def set_parent(self, value: map_node):
        self.parent = value
