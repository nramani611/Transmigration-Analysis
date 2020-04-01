class Cell(object):

    cell_number = 0

    def __init__(self, current_loc, old_loc = (0, 0), migration = False, time = 0):
        Cell.cell_number += 1
        self.current_loc = current_loc
        self.migration = migration
        self.time = time
        self.cell_number = Cell.cell_number
        self.old_loc = old_loc

    def get_cell_number(self):
        return self.cell_number

    def set_time(self, time):
        self.time = time

    def add_time(self, time):
        self.time += time

    def get_time(self):
        return self.time

    def get_number(self):
        return cell_number

    def set_loc(self, current_loc):
        self.old_loc = self.current_loc
        self.current_loc = current_loc

    def get_current_loc(self):
        return self.current_loc

    def get_old_loc(self):
        return self.old_loc

    def set_transmigration(self, migration):
        self.migration = migration

    def get_transmigration(self, migration):
        return self.transmigration

    def __str__(self):
        return str(self.cell_number) + ", "  + str(self.old_loc) + ", " + str(self.current_loc) + ", " + str(self.migration) + ", " + str(self.time)
