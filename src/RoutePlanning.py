import googlemaps
import re
from itertools import permutations

API_KEY = '<Isi dengan API Key>'

gmaps = googlemaps.Client(API_KEY)

def promptOriginPoint():
    origin = input("Masukan tempat awal kamu: ")
    print(f"Alamat yang kamu masukan: {gmaps.geocode(origin)[0]['formatted_address']}")
    return origin

def kosanPoint():
    amountKos = int(input("Masukan banyaknya kos yang ingin kamu survey: "))
    amountPlaces = amountKos + 1
    semuaKos = []

    for i in range(amountKos):
        tempKos = input(f"Masukan kos ke-{i + 1}: ")
        semuaKos.append(tempKos)
        print(f"Alamat yang kamu masukan: {gmaps.geocode(tempKos)[0]['formatted_address']}")

    return amountPlaces, semuaKos

# Parameter choice: 'distance' or 'duration'
def measureTool(origin, destination, choice):
    tempInfo = gmaps.distance_matrix(origin, destination)
    tempDistance = tempInfo['rows'][0]['elements'][0][choice]['text']
    result = float(re.sub("[^0-9.\-]","", tempDistance))
    return result

def generateMatrix(origin, amountPlaces, semuaKos):
    matrixAdj = [[0 for _ in range(amountPlaces)] for _ in range (amountPlaces)]
    for i in range(amountPlaces):
        for j in range(amountPlaces):
            if(i != j):
                if(i == 0):
                    matrixAdj[i][j] = measureTool(origin, semuaKos[j - 1], 'distance')
                else:
                    if(j == 0):
                        matrixAdj[i][j] = measureTool(semuaKos[i - 1], origin, 'distance')
                    else:
                        matrixAdj[i][j] = measureTool(semuaKos[i - 1], semuaKos[j - 1], 'distance')
    return matrixAdj

def TSPBruteforce(matrix, r, size):
    global funcCall
    node = []
    dict = {}
    for i in range(size):
        if i != r:
            node.append(i)

    permutate = permutations(node)
    res = float('inf')
    for val in permutate:
        j = 0
        k = r
        for l in val:
            j += matrix[k][l]
            k = l
        j += matrix[k][r]
        res = min(j, res)
        dict[val] = res
    return res, list(dict.keys())[list(dict.values()).index(res)]

def TranslateResult(res, origin, semuaKos):
    print("Hasil optimasi rute:")
    path = []
    path.append(origin)
    for seq in res:
        path.append(semuaKos[seq - 1])
    path.append(origin)
    
    for i in range(len(path)):
        if i == len(path) - 1:
            print(path[i])
        else:
            print(path[i], end = " -> ")

if __name__ == '__main__':
    origin = promptOriginPoint()
    amountPlaces, dest = kosanPoint()

    matrixAdj = generateMatrix(origin, amountPlaces, dest)
    minimumVal, result = TSPBruteforce(matrixAdj, 0, amountPlaces)
    TranslateResult(result, origin, dest)
    print("Total ")