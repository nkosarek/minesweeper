import random


class Game:
    def __init__(self):
        self.board = None
        self.is_win = None
        self.play = True

    def start(self):
        while self.play:
            self._setup()
            while self.is_win is None:
                self._draw_board_and_prompt_move()

            self._draw_board_and_complete()
            self._prompt_play_again()

    def _setup(self):
        rows, cols, mines = self._prompt_setup()
        self.board = Board(rows, cols, mines)

    @staticmethod
    def _prompt_setup():
        print "********************************************"
        print "Please input number of rows, columns, and mines:"
        rows = Game._prompt_get_value("rows", 2, 10)
        cols = Game._prompt_get_value("cols", 2, 10)
        max_mines = (rows * cols) / 4
        mines = Game._prompt_get_value("mines", 1, max_mines)
        return rows, cols, mines

    @staticmethod
    def _prompt_get_value(name, min_val, max_val):
        val = min_val - 1
        fail_msg = "Invalid value for " + name + ". Must be between " + \
            str(min_val) + " and " + str(max_val) + " inclusive"

        while val < min_val or val > max_val:
            val_str = raw_input(name + ": ")
            try:
                val = int(val_str)
            except:
                val = min_val - 1
            if val < min_val or val > max_val:
                print fail_msg
        return val

    def _draw_board_and_prompt_move(self):
        print "********************************************"
        self.board.draw()
        valid_loc = False
        while not valid_loc:
            print "Pick the row and column of a tile to reveal:"
            row = Game._prompt_get_value("row", 0, self.board.num_rows - 1)
            col = Game._prompt_get_value("col", 0, self.board.num_cols - 1)
            if self.board.tiles[row][col].is_revealed:
                print "Tile at (%d, %d) already revealed" % (row, col)
            else:
                valid_loc = True
        if not self.board.reveal_tiles(row, col):
            self.is_win = False
        elif self.board.is_cleared():
            self.is_win = True

    def _draw_board_and_complete(self):
        print "********************************************"
        self.board.draw()
        if self.is_win:
            print "*** SUCCESS ***"
        else:
            print "*** FAILURE ***"

    def _prompt_play_again(self):
        response = raw_input("Play again? (y/n): ")
        if response != "y":
            self.play = False
            print "Thanks for playing!"
        else:
            self.board = None
            self.is_win = None


class Board:
    def __init__(self, num_rows, num_cols, num_mines):
        self.tiles = []
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_revealed = 0
        # Create empty tiles
        for row in xrange(num_rows):
            self.tiles.append([])
            for col in xrange(num_cols):
                self.tiles[row].append(Tile())
        # Determine where mines are
        self.mines = Board._generate_mines(num_rows, num_cols, num_mines)
        # self.mines = [(0,2), (1,2), (2,0), (3,1)]
        # Place mines
        for (row, col) in self.mines:
            self.tiles[row][col].is_mine = True
            # Update adjacent_mines variable for all tiles around this mine
            adjacent_tiles = self._get_adjacent_unrevealed_tiles(row, col)
            for (r, c) in adjacent_tiles:
                self.tiles[r][c].adjacent_mines += 1

    @staticmethod
    def _generate_mines(num_rows, num_cols, num_mines):
        mine_indices = random.sample(xrange(num_rows * num_cols), num_mines)
        mine_locations = []
        for idx in mine_indices:
            mine_locations.append((idx / num_cols, idx % num_cols))
        return mine_locations

    def _get_adjacent_unrevealed_tiles(self, row, col):
        adjacent_tiles = []
        for r in xrange(row - 1, row + 2):
            if r < 0 or r >= self.num_rows:
                continue
            for c in xrange(col - 1, col + 2):
                if c < 0 or c >= self.num_cols or (r == row and c == col):
                    continue
                if not self.tiles[r][c].is_revealed:
                    adjacent_tiles.append((r, c))
        return adjacent_tiles

    def reveal_tiles(self, start_row, start_col):
        if self.tiles[start_row][start_col].is_mine:
            self.reveal_all_mines()
            return False

        to_reveal = [(start_row, start_col)]
        processed = set((start_row, start_col))
        while len(to_reveal) > 0:
            row, col = to_reveal[0]
            curr_tile = self.tiles[row][col]
            reveal_more = curr_tile.reveal()
            self.num_revealed += 1
            if reveal_more:
                adj_tiles = self._get_adjacent_unrevealed_tiles(row, col)
                for tile_loc in adj_tiles:
                    if tile_loc not in processed:
                        to_reveal.append(tile_loc)
                        processed.add(tile_loc)

            to_reveal.pop(0)
        return True

    def reveal_all_mines(self):
        for (row, col) in self.mines:
            self.tiles[row][col].reveal()

    def draw(self):
        for row in xrange(-2, self.num_rows):
            row_display = ""
            for col in xrange(-2, self.num_cols):
                if row < 0 and col < 0:
                    row_display += " "
                elif row == -2:
                    row_display += str(col)
                elif row == -1:
                    row_display += "-"
                elif col == -2:
                    row_display += str(row)
                elif col == -1:
                    row_display += "|"
                else:
                    curr_tile = self.tiles[row][col]
                    tile_display = "+"
                    if curr_tile.is_revealed and curr_tile.is_mine:
                        tile_display = "X"
                    elif curr_tile.is_revealed and curr_tile.adjacent_mines == 0:
                        tile_display = " "
                    elif curr_tile.is_revealed:
                        tile_display = str(curr_tile.adjacent_mines)
                    row_display += tile_display
            print row_display

    def is_cleared(self):
        num_tiles = self.num_rows * self.num_cols
        if num_tiles - len(self.mines) > self.num_revealed:
            return False
        return True


class Tile:
    def __init__(self):
        self.is_mine = False
        self.adjacent_mines = 0
        self.is_revealed = False

    def reveal(self):
        self.is_revealed = True
        return self.adjacent_mines == 0 and not self.is_mine


if __name__ == "__main__":
    print "*** MINESWEEPER ***"
    game = Game()
    game.start()
