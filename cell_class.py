class Cell(object):

    cell_number = 0

    def __init__(self, loc, migration = False, time = 0):
        Cell.cell_number += 1
        self.loc = loc
        self.migration = migration
        self.time = time
        self.cell_number = Cell.cell_number

    def set_time(self, time):
        self.time = time

    def add_time(self, time):
        self.time += time

    def get_time(self):
        return self.time

    def get_number(self):
        return cell_number

    def set_loc(self, loc):
        self.loc = loc

    def get_loc(self):
        return self.loc

    def set_transmigration(self, migration):
        self.migration = migration

    def get_transmigration(self, migration):
        return self.transmigration

    def __str__(self):
        return str(self.cell_number) + " "  + str(self.loc) + " " + str(self.migration) + " " + str(self.time)
