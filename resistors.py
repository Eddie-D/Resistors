import json
from fractions import Fraction

def read_sets(path="resistances.json") :
    print("Reading the file...")
    try :
        with open(path, "r") as f :
            sets = json.load(f)
        sets = [{Fraction(k):v for k, v in s.items()} for s in sets]

    except Exception as e :
        print("Excepted")
        print(e)
        sets = None

    if not sets :
        sets = [{Fraction(1):"r"}]

    print("File read")
    return sets

def construct(type, x, y) :
    if x[0] == type :
        x = x[2:-1]
    if y[0] == type :
        y = y[2:-1]
    return f"{type}({x} {y})"

def calculate_next(sets) :
    sn = {}
    pairs = []
    for i in range(len(sets) // 2) :
        pairs.append((i, len(sets) - 1 - i))
    if len(sets) % 2 == 1 :
        mid = len(sets) // 2
        pairs.append((mid,mid))

    for pair in pairs :
        s1,s2 = sets[pair[0]], sets[pair[1]]
        for x, x_construct in s1.items() :
            for y, y_construct in s2.items() :
                pkey = Fraction(x*y, x+y)
                if pkey not in sn :
                    sn[pkey] = construct("P", x_construct, y_construct)

                skey = Fraction(x + y)
                if skey not in sn :
                    sn[skey] = construct("S", x_construct, y_construct)

    sets.append(sn)

def find_occurences(f, sets) :
    occurs = []
    for i, s in enumerate(sets) :
        if f in s :
            occurs.append(i+1)
    return occurs

def get_construction(n, f, sets) :
    if f not in sets[n - 1] :
        return None
    
    return sets[n-1][f]

def print_constructions(f, sets) :
    occurs = find_occurences(f, sets)
    for n in occurs :
        print(f"In S[{n}]: {f} = {get_construction(n, f, sets)}")

def dump_sets(sets, path="resistances.json") :
    # Convert Fraction keys to strings for JSON serialization
    sets_serializable = [{str(k): v for k, v in s.items()} for s in sets]

    print("Dumping, DO NOT EXIT")
    with open(path, "w") as f :
        json.dump(sets_serializable, f, indent=4)

'''
for i in range(10) :
    print(i)
    calculate_next(sets)
'''

sets = read_sets()

# calculate_next(sets)
# dump_sets(sets)

lengths = list(map(len, sets))
print(f"Lengths: {lengths}")

print(f"The number 1 can be made with: {find_occurences(Fraction(1), sets)} resistors")
print(f"The number 1 can be made with 4 resistors by: {get_construction(4, Fraction(1), sets)}")
print_constructions(Fraction(1), sets)
