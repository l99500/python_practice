import shutil
import zipfile
from pathlib import Path


class ZipProcessor:
    def __init__(self, zip_name):
        self.zip_name = zip_name
        self.temp_directory = Path("unzipped-{}".format(zip_name[:-4]))

    def process_zip(self):
        self.unzip_files()
        self.process_files()
        self.zip_files()

    def unzip_files(self):
        self.temp_directory.mkdir()
        with zipfile.ZipFile(self.zip_name) as zip_:
            zip_.extractall(str(self.temp_directory))

    def zip_files(self):
        with zipfile.ZipFile(self.zip_name, 'w') as file:
            for filename in self.temp_directory.iterdir():
                file.write(str(filename), filename.name)
            shutil.rmtree(str(self.temp_directory))
