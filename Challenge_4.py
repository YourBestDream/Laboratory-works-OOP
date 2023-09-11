class Diamond:
    def __init__(self, size):
        self.size = size

    def draw(self):
        if self.size % 2 == 0:
            raise ValueError("Size must be an odd number")

        for i in range(1, self.size + 1):
            if i <= (self.size // 2) + 1:
                spaces = " " * ((self.size // 2) + 1 - i)
                stars = "*" * (2 * i - 1)
            else:
                spaces = " " * (i - (self.size // 2 + 1))
                stars = "*" * (2 * (self.size - i) + 1)

            print(spaces + stars)

size = 3
diamond = Diamond(size)
diamond.draw()