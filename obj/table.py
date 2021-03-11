class Table:
    def __init__(self, headers: list[str]):
        self.labels = headers
        self.num_columns = len(headers)
        self.rows: list[list]
        self.rows = []
        self._labels_to_index()

    def __getitem__(self, arg):
        """table[label, value] -> list of rows"""
        assert len(arg) == 2
        label, value = arg
        index = self.index_of(label)
        matches = []
        for row in self.rows:
            if row[index] == value:
                matches.append(row)
        if matches:
            return tuple(matches)
        else:
            raise KeyError(f"Can't find value {value} in column {label}.")

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        widths = self.column_widths()
        pretty_rows = []
        header = True
        for row in ([list(self.labels)] + self.rows):
            pretty_items = []
            for i, content in enumerate(row):
                pretty = str(content).rjust(widths[i])
                pretty_items.append(" " + pretty + " ")
            pretty_rows.append("|".join(pretty_items))
            if header:
                line = "=" * len(pretty_rows[0])
                pretty_rows.append(line)
                header = False
        return "\n".join(pretty_rows)
        

    def add_row(self, row):
        if len(row) != self.num_columns:
            raise Exception("Given row doesn't have same number of columns as table!")
        self.rows.append(list(row))

    def _labels_to_index(self):
        self.label_index = {}
        for i, label in enumerate(self.labels):
            self.label_index[label] = i

    def index_of(self, label):
        return self.label_index[label]

    def copy_column(self, label=None, index=None):
        """input either column name or column index"""
        def row_get_val(row, index):
            return row[index]
        if label:
            index = self.index_of(label)
        return tuple(map(lambda row, i=index: row_get_val(row, i), self.rows))

    def column_widths(self):
        widths = [0 for i in range(self.num_columns)]
        for row in ([list(self.labels)] + self.rows):
            for i in range(self.num_columns):
                width = len(str(row[i]))
                widths[i] = width if width > widths[i] else widths[i]
        return widths
            

if __name__ == '__main__':

    t = Table("i name color".split())
    t.add_row([1, "james", "blue"])
    t.add_row([2, "john", "red"])
    t.add_row([3, "jan", "pink"])

    t["i",3][0][2] = "blackaaaaa"

    c = t.copy_column("color")