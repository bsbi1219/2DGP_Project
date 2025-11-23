class Wall:
    def __init__(self, left, bottom, right, top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top

    def get_bb(self):
        return self.left, self.bottom, self.right, self.top

    def update(self):
        pass

    def draw(self):
        pass

    def handle_collision(self, group, other):
        pass