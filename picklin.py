# Thanks to StackOverflow user Zah: https://stackoverflow.com/questions/19201290/how-to-save-a-dictionary-to-a-file

import pickle

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)