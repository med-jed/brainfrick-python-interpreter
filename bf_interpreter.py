bf_file = open("brainfuck.txt", "r")
bf_symbols = ["<", ">", "+", "-", ".", ",", "[", "]"]

bf_commands = []

for char in bf_file.read():
    if char in bf_symbols:
        bf_commands.append(char)

class Interpreter:
    def __init__(self, commands):
        '''
        This is an object that is able to translate a working brainf*** program
        into Python functions.

        Currently, as of August/28/2021, the , symbol has not yet been implemented.
        '''
        self.bf_program = commands
        # The index of the original bf program itself.
        self.bf_index = 0

        # Is actually 30000 cells in actual brainf***. I'll make it ~20 for testing's sake.
        self.memory_cells = [0] * 20
        self.pointer = 0
        # The positions of left-sided brackets and the current one selected in the array.
        self.left_bracket_indexes = []
        self.left_bracket_index = 0

        # The positions of right-sided brackets and the current one selected in the array.
        self.right_bracket_indexes = []
        self.right_bracket_index = -1

        # What we will output in the end!
        self.interpreted_message = ""

    def decrement_pointer(self):
        self.pointer -=1

    def increment_pointer(self):
        self.pointer += 1

    def increment_cell(self):
        self.memory_cells[self.pointer] += 1

    def decrement_cell(self):
        self.memory_cells[self.pointer] -= 1

    def get_character(self, value):
        self.interpreted_message += str(chr(value))

    def input_character(self, value):
        # Not sure how to implement this...
        pass

    def loop(self, left_bracket_index, right_bracket_index):
        '''For the brackets.
        Let left_bracket_index be the point in the
        bf program where the loop starts and 
        right_bracket_index be where the loop ends.

        If the value of the cell is nonzero 
        when you're at the right bracket index,
        return to the matching left bracket.

        But if the cell at the pointer is zero 
        when you are at the left bracket index,
        move the pointer to right_bracket_index += 1.
        '''
        # print(self.bf_program[self.bf_index])

        # Increment left and .
        self.left_bracket_index += 1
        self.right_bracket_index += 1
        if self.left_bracket_index == len(self.left_bracket_indexes):
            # We make it 1 and 0 because the main loop isn't finished.
            # If you're starting a new, non-nested loop,
            # self.left_bracket_index would be 0 and
            # self.right_bracket_index would be -1.
            self.left_bracket_index = 1
            self.right_bracket_index = 0

        # When this value is 0, we can stop the loop.
        memory_cell_val = self.memory_cells[self.pointer]
        # print("Memory cell ", self.pointer, " value: ", self.memory_cells[self.pointer], "Right bracket pointer: ", right_bracket_index)
        while memory_cell_val != 0:
            # You should already be on the bf_index of the left bracket of the loop, so add one for the next symbol
            self.bf_index += 1

            self.interpret()
            # print("Bf index: ", self.bf_index, " Right bracket index: ", right_bracket_index, " Left bracket index: ", left_bracket_index)
            if self.bf_index == right_bracket_index:
                memory_cell_val = self.memory_cells[self.pointer]
                if memory_cell_val > 0:
                    self.bf_index = left_bracket_index  # Reset the index to the position of the left bracket of the loop.
                # print("Cell: ", self.pointer, " Cell value: ", self.memory_cells[self.pointer])
        # When the loop is finished, leave the bf_index at the position of the last right bracket.
        self.bf_index = right_bracket_index

    def interpret(self):
        symbol = self.bf_program[self.bf_index]
        # print(self.left_bracket_index, self.right_bracket_index, self.left_bracket_indexes, self.right_bracket_indexes)
        # print(symbol, " ", self.memory_cells, "BF index value ", self.bf_index)
        if symbol == bf_symbols[0]:  # <
            self.decrement_pointer()
        elif symbol == bf_symbols[1]:  # >
            self.increment_pointer()
        elif symbol == bf_symbols[2]:  # +
            self.increment_cell()
        elif symbol == bf_symbols[3]:  # -
            self.decrement_cell()
        elif symbol == bf_symbols[4]:  # .
            self.get_character(self.memory_cells[self.pointer])
        elif symbol == bf_symbols[5]:  # , (Not implemented!)
            self.input_character(self.memory_cells[self.pointer])
        elif symbol == bf_symbols[6]:  # [
            # print("Looping")
            # We save the position of the left bracket and the right bracket in our loop function.
            self.loop(self.left_bracket_indexes[self.left_bracket_index], self.right_bracket_indexes[self.right_bracket_index])

    def brackets_management(self, init_index):
        '''
        A function to store and remove brackets in lists as needed.
        From the starting index number, it will run through the entirety of the bf program
        and save any left brackets and right brackets until the number of left and right brackets
        is equal.

        The general rule is the first left bracket corresponds with the last right bracket,
        the second left bracket and the first right bracket, and so on.
        '''
        search_index = init_index
        # print(search_index)

        # Once we've gone past the index of a set of brackets in the bf program,
        # we can go ahead and clear them from the lists.
        if len(self.right_bracket_indexes) > 0:
            if self.bf_index >= self.right_bracket_indexes[-1]:
                self.left_bracket_indexes.clear()
                self.right_bracket_indexes.clear()

        if len(self.left_bracket_indexes) == 0:
            if self.bf_program[search_index] == "[":
                # Add the index of a left bracket the program will encounter
                self.left_bracket_indexes.append(search_index)
                search_index += 1

        # Then, we will search for the first left bracket's corresponding right bracket
        # As well as take any brackets between them.
        while len(self.left_bracket_indexes) != len(self.right_bracket_indexes):
            if self.bf_program[search_index] == "[":
                # Add the indexes of left brackets in the bf_program to left_bracket_indexes.
                self.left_bracket_indexes.append(search_index)
            elif self.bf_program[search_index] == "]":
                # Add the index of the right brackets in the bf_program to right_bracket_indexes.
                self.right_bracket_indexes.append(search_index)
            search_index += 1
            #print("Left brackets indexes: ", self.left_bracket_indexes, "Right brackets indexes: ", self.right_bracket_indexes)

            # Once we find the left and right brackets, we reset the indexes of the left and right brackets.
            self.left_bracket_index = 0
            self.right_bracket_index = -1
        self.bf_index = init_index

interpreter = Interpreter(bf_commands)
while len(bf_commands) > interpreter.bf_index:
    interpreter.brackets_management(interpreter.bf_index)
    interpreter.interpret()
    interpreter.bf_index += 1

# print(interpreter.left_bracket_indexes, interpreter.right_bracket_indexes)
print(interpreter.memory_cells)
print(interpreter.interpreted_message)
# print(interpreter.bf_index)
# print(interpreter.pointer)