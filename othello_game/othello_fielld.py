from tile import Tile


class OthelloField:
    def __init__(self, FIELD_SIZE, CELL_SIZE):
        self.FIELD_SIZE = FIELD_SIZE
        self.CELL_SIZE = CELL_SIZE
        self.STROKE_WEIGHT = 3
        self.COLOR_W = 255
        self.COLOR_B = 0
        self.curr_color = self.COLOR_B
        self.count_b = 0
        self.count_w = 0
        self.TIMER = 150
        self.count_down = self.TIMER
        self.neighbors = [-1, 0, 1]
        self.legal_list = []
        self.search_posi_list = []
        self.searched_posi = []
        self.no_valid_move = 0
        self.game_end = False
        self.asked_name = False

        # Initialize the tile table, all spots are empty
        # [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.tile_table = [[0] * self.FIELD_SIZE
                           for i in range(self.FIELD_SIZE)]

        # Initialize the first 4 piles in the middle when the game start
        for x in range(self.FIELD_SIZE//2 - 1, self.FIELD_SIZE//2 + 1):
            for y in range(self.FIELD_SIZE//2 - 1, self.FIELD_SIZE//2 + 1):
                self.opp_curr_color()
                self.tile_table[x][y] = Tile(x, y, self.curr_color)
            self.opp_curr_color()
        # curr_color is black now, it's the next player's color

    def display(self):
        # The field of the game
        STROKE_WEIGHT = self.STROKE_WEIGHT
        CELL_SIZE = self.CELL_SIZE
        FIELD_SIZE = self.FIELD_SIZE

        background(0, 150, 0)  # Set the background to dark green
        stroke(0, 0, 0)
        strokeWeight(STROKE_WEIGHT)
        # Draw the backgrond grid
        for _ in range(self.FIELD_SIZE + 1):
            line(_ * CELL_SIZE, 0, _ * CELL_SIZE, CELL_SIZE * FIELD_SIZE)
            line(0, _ * CELL_SIZE, CELL_SIZE * FIELD_SIZE, _ * CELL_SIZE)

        self.draw_tiles()

        if not self.game_end:
            self.update()
        else:
            self.announce_winner()
            # Ask for the user's name once
            if not self.asked_name:
                self.count_down -= 1
                # Wait for the count down
                # So if the white place the last move
                # The pile can be placed before anounce result.
                if self.count_down == 0:
                    self.draw_tiles()
                    self.record_user_score()
                    self.asked_name = True

    def draw_tiles(self):
        # Count the number of black and white
        # and display the piles
        CELL_SIZE = self.CELL_SIZE
        FIELD_SIZE = self.FIELD_SIZE
        self.count_b = 0
        self.count_w = 0
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                if self.tile_table[i][j]:
                    if self.tile_table[i][j].color == self.COLOR_B:
                        self.count_b += 1
                    else:
                        self.count_w += 1
                    self.tile_table[i][j].display()

    def opp_curr_color(self):
        # Change the curr_color to the opposite
        if self.curr_color == self.COLOR_B:
            self.curr_color = self.COLOR_W
        else:
            self.curr_color = self.COLOR_B

    def place_black_tile(self, x, y):
        # See what color it is
        # If it is Black, place the tile
        if self.curr_color == self.COLOR_B:
            self.place_tile(x, y)
            # Change the color to white

    def place_tile(self, x, y):
        # If the spot already have pile
        # Can not place another one
        if self.tile_table[x][y]:
            return

        # If the tile is not legal
        # return
        if (x, y) in self.legal_list:
            self.tile_table[x][y] = Tile(x, y, self.curr_color)
            self.flip_tile(x, y)
            self.opp_curr_color()
            self.search_posi_list = []
            self.legal_list = []
            self.no_valid_move = 0

    def update(self):
        # Update the field
        self.create_legal_list()
        player = "Black"
        # If there's still legal move?
        if not self.legal_list and self.no_valid_move < 2:
            self.no_valid_move += 1
            if self.curr_color == self.COLOR_W:
                player = "White"
            print("No legal move for " + player)
            self.opp_curr_color()
            return

        # If it is the computer's turn
        if self.curr_color == self.COLOR_W:
            player = "White"
            self.count_down -= 1
            if self.count_down == 0:
                # Use my AI to fill in the value x y in it
                # Choose the next move with the most
                # number of white tiles to be flipped.
                if self.legal_list:
                    # next_step = len(self.legal_list) // 2
                    # (x, y) = self.legal_list[next_step]
                    (x, y) = self.find_max_to_flip()
                    self.place_tile(x, y)
                    self.count_down = self.TIMER

        # Announce player on the right top
        fill(255)
        textSize(25)
        field_size = self.FIELD_SIZE * self.CELL_SIZE
        present_player = "It's " + player + "\'s turn."
        text(present_player, field_size - 200, 100)

        # If the field is full
        if self.no_valid_move == 2:
            pass
        else:
            for i in self.tile_table:
                for j in i:
                    # If one cell is empty
                    if not j:
                        return

        self.game_end = True
        self.display()

    def record_user_score(self):
        # promote the user for name
        # record their score in file
        answer = str(self.input("Please enter your name: "))
        answer_score = answer + " " + str(self.count_b)
        top_score = -1
        with open('scores.txt', 'r+') as f:
            countent = f.readline()
            countent = countent.split(" ")
            if len(countent) > 1:
                top_score = int(countent[-1])
        with open('scores.txt', 'r+') as f:
            former_scores = f.read()
            if top_score == -1:
                f.write(answer_score)
            elif self.count_b > top_score:
                f.seek(0, 0)
                f.write(answer_score + "\n" + former_scores)
            else:
                f.seek(0, 0)
                f.write(former_scores + "\n" + answer_score)

    def input(self, message=''):
        from javax.swing import JOptionPane
        return JOptionPane.showInputDialog(frame, message)

    def announce_winner(self):
        # Compare and print the result
        if self.count_b > self.count_w:
            result = "BLACK WIN"
            num_t = self.count_b
        elif self.count_b < self.count_w:
            result = "WHITE WIN"
            num_t = self.count_w
        else:
            result = " IT'S A TIE"
            num_t = self.count_b

        # Announce the result on screen
        fill(0, 0, 255)
        textSize(60)
        field_size = self.FIELD_SIZE * self.CELL_SIZE/2
        text(result, field_size - 150, field_size - 50)
        textSize(40)
        text("With the number of: " + str(num_t) + " tiles.",
             field_size - 290, field_size + 40)

    # Here below create a list of legal move for the next move.
    def create_legal_list(self):
        # Create a list of position that is legal for this player

        # Define opposite color
        if self.curr_color == self.COLOR_B:
            opp_color = self.COLOR_W
        else:
            opp_color = self.COLOR_B

        # Find tiles with opposite color
        for column in self.tile_table:
            for grid in column:
                if grid:
                    if grid.color == opp_color:
                        x = grid.column
                        y = grid.row
                        self.search_posi(x, y, self.curr_color, opp_color)
                        self.search_empt_posi(self.curr_color, opp_color)

    def search_posi(self, x, y, curr_color, opp_color):
        # Find the positions to be search
        # save in search_posi_list
        for i in self.neighbors:
            for j in self.neighbors:
                if not (i == 0 and j == 0):
                    m, n = x + i, y + j
                    if self.is_in_field(m, n):
                        # Find empty grid near opp_color
                        if not self.tile_table[m][n]:
                            if (m, n) not in self.search_posi_list:
                                self.search_posi_list.append((m, n))

    def search_empt_posi(self, curr, opp):
        # Search though all the spaces that been found
        for (x, y) in self.search_posi_list:
            for i in self.neighbors:
                for j in self.neighbors:
                    if not (i == 0 and j == 0):
                        m, n = x + i, y + j
                        if self.is_in_field(m, n) and self.tile_table[m][n]:
                            # If there's one with opposite color
                            # Keep seaching in that direction
                            if self.tile_table[m][n].color == opp:
                                if self.search_one_more(m, n, i, j, curr, opp)\
                                   and ((x, y) not in self.legal_list):
                                    self.legal_list.append((x, y))

    def search_one_more(self, x, y, i, j, curr, opp):
        # Keep seaching in the direction (+i, +j)
        # Until reach a curr_color or empty cell
        if not self.is_in_field(x + i, y + j):
            return False
        if not self.tile_table[x + i][y + j]:
            return False

        if self.tile_table[x + i][y + j].color == curr:
            return True
        elif self.tile_table[x + i][y + j].color == opp:
            return self.search_one_more(x + i, y + j, i, j, curr, opp)

    # This part flip the tile
    # When there's a move
    def flip_tile(self, x, y):
        # Flip the tile in between two tiles

        # Define opposite color
        curr = self.curr_color
        if curr == self.COLOR_B:
            opp = self.COLOR_W
        else:
            opp = self.COLOR_B

        # Find the tiles and flip it
        for i in self.neighbors:
            for j in self.neighbors:
                m, n = x + i, y + j
                if (not (i == 0 and j == 0))\
                   and (self.is_in_field(m, n))\
                   and (self.tile_table[m][n]):
                    # If the color is opposite
                    # and it's a valid direction
                    if self.tile_table[m][n].color == opp\
                       and self.search_one_more(m, n, i, j, curr, opp):
                        while self.tile_table[m][n].color == opp:
                            self.tile_table[m][n].color = curr
                            m += i
                            n += j

    # Below is the implementation for "AI"
    def find_max_to_flip(self):
        # Find the move that filp the maximum
        # number of tiles with opposite color
        num_to_flipped = 0
        m, n = 0, 0
        for (x, y) in self.legal_list:
            num_flipped = self.num_flipped(x, y)
            if self.num_flipped(x, y) > num_to_flipped:
                num_to_flipped = num_flipped
                m, n = x, y
        return m, n

    def num_flipped(self, x, y):
        num_flip = 0
        # Define opposite color
        curr = self.curr_color
        if curr == self.COLOR_B:
            opp = self.COLOR_W
        else:
            opp = self.COLOR_B

        # Find the tiles and count it
        for i in self.neighbors:
            for j in self.neighbors:
                m, n = x + i, y + j
                if (not (i == 0 and j == 0))\
                   and (self.is_in_field(m, n))\
                   and (self.tile_table[m][n]):
                    # If the color is opposite
                    # and it's a valid direction
                    if self.tile_table[m][n].color == opp\
                       and self.search_one_more(m, n, i, j, curr, opp):
                        while self.tile_table[m][n].color == opp:
                            num_flip += 1
                            m += i
                            n += j
        return num_flip

    def is_in_field(self, x, y):
        # Determine if a scale is in field or not
        if x >= 0 and x < self.FIELD_SIZE and y >= 0 and y < self.FIELD_SIZE:
            return True
        return False
