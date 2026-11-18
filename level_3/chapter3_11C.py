class FileManager:
    def __init__(self,filename):
        self.filename=filename

    def read_data(self):
        with open(self.filename,'r') as file:
            return file.read().strip()

    def write_data(self,data):
        with open(self.filename,'w') as file:
            file.write(data)
            return len(data
                       )
