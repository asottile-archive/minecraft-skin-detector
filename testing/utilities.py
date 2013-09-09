
import config
import os.path

def get_datafile(datafile_name):
    filename = os.path.join(config.BASE_PATH, 'testing/data', datafile_name)
    with open(filename, 'r') as datafile:
        return datafile.read()
