import sys
class TempOut:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, 'w')

        self.old_stdout = sys.stdout
        sys.stdout = self.file
    

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self.old_stdout
        self.file.close()


with TempOut('output.txt') as to:
    # enter is run
    print(to)
    print("This will be written to the file 'output.txt'")
    print("This is another line that will be written to the file.")
    # exit is run