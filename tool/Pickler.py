# Thanks to StackOverflow user Zah: https://stackoverflow.com/questions/19201290/how-to-save-a-dictionary-to-a-file
import pickle


class Pickler:

    @staticmethod
    def save_obj(obj, path_to_save_obj):
        with open(path_to_save_obj, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_obj(path_to_object):
        with open(path_to_object, 'rb') as f:
            return pickle.load(f)
