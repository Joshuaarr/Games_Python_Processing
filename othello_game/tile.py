class Tile:
    # Define one tile
    def __init__(self, column, row, color):
        self.column = column
        self.row = row
        self.color = color

    def display(self):
        # Display a single tile
        color = self.color
        fill(color)
        column = self.column
        row = self.row
        ellipse(self.column * 100 + 50, self.row * 100 + 50, 90, 90)
