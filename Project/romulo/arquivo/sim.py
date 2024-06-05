import pickle
from datasketch import MinHash, MinHashLSH
from nltk.metrics import jaccard_distance


with open("../mol_bits.pkl", "rb") as f:
    MOL_BITS = pickle.load(f)

LSH = MinHashLSH(threshold=0.5, num_perm=256)

# Função para criar MinHash a partir de uma lista de valores
def create_minhash(values):
    m = MinHash(num_perm=256)
    for val in values:
        m.update(str(val).encode('utf8'))
    return m

for key, values in MOL_BITS.items():
    m = create_minhash(values)
    LSH.insert(key, m)


def find_similar_keys(target_key, threshold=0.5):
    target_minhash = create_minhash(MOL_BITS[target_key])
    result = LSH.query(target_minhash)
    toReturn = {}
    for key in result:
        if key == target_key:
            continue
        score = 1 - jaccard_distance(set(MOL_BITS[target_key]), set(MOL_BITS[key]))
        if score > threshold:
            toReturn[key] = score

    return toReturn

