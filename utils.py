import json
import numpy as np
import os


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """

    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32,
                              np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def load_config(filename="config"):
    """ Function to load a configuration file """

    with open("config/{}.json".format(filename)) as cfg:
        config = json.load(cfg)
    return config


def save_as_json(data, filepath, name_extension):
    filename = build_filename(filepath, name_extension)
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, cls=NumpyEncoder, sort_keys=False, indent=4, ensure_ascii=False)


def build_filename(filepath, name_extension):
    base_name = os.path.splitext(filepath)[0]
    filename = base_name.replace("BalanceBoard_Static", "results") + "_{}.json".format(name_extension)
    dir_name = os.path.dirname(filename)
    check_folder(dir_name)

    return filename


def check_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def get_path_to_all_files(folder_name):
    filepaths = []
    for dirname, dirnames, filenames in os.walk(folder_name):
        for filename in filenames:
            if '.DS_Store' not in filename:
                filepaths.append(os.path.join(dirname, filename))

    return filepaths
