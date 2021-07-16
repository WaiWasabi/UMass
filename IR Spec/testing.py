import pickle

valid_dir = 'Dataset/valid'
invalid_dir = 'Dataset/invalid'

with open(valid_dir, 'rb') as data:
    valid = pickle.load(data)

with open(invalid_dir, 'rb') as data:
    invalid = pickle.load(data)

key = list(valid.keys())

for i in range(10):
    print(f'{key[i]}: {valid[key[i]][0]}\n{valid[key[i]][1]}\n{valid[key[i]][2:]}')
