import random


def reverseString(string):
    reversedString = ""
    for i in range(len(string) - 1,-1,-1):
        reversedString += string[i]
    return reversedString


def randomStringGenerator():
    randomString = ""
    randomlist = random.sample(range(19, 127), 8)
    for num in randomlist:
        randomString += chr(num)
    return randomString

def convertHexaToBinary(string):
    binaryText = ""
    for char in string:
        num = 0
        if char == "F":
           num = 15
        elif char == "E":
            num = 14
        elif char == "D":
           num = 13
        elif char == "C":
           num = 12
        elif char == "B":
           num = 11
        elif char == "A":
           num = 10
        else:
            num = int(char)
        binaryChar = ""
        while num > 0:
            binaryChar += str(num % 2)
            num = int(num / 2)
        while(len(binaryChar) < 4):
            binaryChar += "0"
        binaryText += reverseString(binaryChar)
    return binaryText


def convertStringToHexadecimal(string):
    hexaText = ""
    for char in string:
        num = ord(char)
        hexaChar = ""
        while num > 0 :
            if num % 16 < 10:
                hexaChar += str(num % 16)
            if num % 16 == 10:
                hexaChar += "A"
            if num % 16 == 11:
                hexaChar += "B"
            if num % 16 == 12:
                hexaChar += "C"
            if num % 16 == 13:
                hexaChar += "D"
            if num % 16 == 14:
                hexaChar += "E"
            if num % 16 == 15:
                hexaChar += "F"
            num = int (num / 16)
        hexaText += reverseString(hexaChar)
    return hexaText

def leftShift(string,num):
    shiftedString = ""
    for j in range(num, len(string)): shiftedString += string[j]
    shiftedString += string[0]
    shiftedString += string[1] if num == 2 else ""
    return shiftedString

def keysProcedures(binaryKey,PC1table,PC2Table,Shift1Table):
    K1permuted = ""
    for num in PC1table:
        K1permuted += binaryKey[num - 1]
    C0 = ""
    D0 = ""
    for i in range(int(len(K1permuted) / 2)): C0 += K1permuted[i]
    for i in range(int(len(K1permuted) / 2), int(len(K1permuted))): D0 += K1permuted[i]
    keyPairs = [[]]
    keyPairs[0].append(C0)
    keyPairs[0].append(D0)
    for i in range(1,16):
        keyPairs.append([])
        keyPairs[i].append(leftShift(keyPairs[i - 1][0],Shift1Table[i - 1]))
        keyPairs[i].append(leftShift(keyPairs[i - 1][1],Shift1Table[i - 1]))
    keys16 = []
    for list in keyPairs:
        keys16.append(list[0] + list[1])
    permutedKeys16 = []
    for key in keys16:
        permKey = ""
        for num in PC2Table:
            permKey += key[num - 1]
        permutedKeys16.append(permKey)
    return permutedKeys16

def getInitialPermutation(message,IPTable):
    perm = ""
    for num in IPTable:
        perm += message[num - 1]
    return perm

def getSplittedMessages(message):
    splittedPieces = []
    counter = 0
    for i in range(int(len(message) / 64)):
        piece = ""
        for j in range(64):
            piece += message[counter]
            counter += 1
        splittedPieces.append(piece)
    return splittedPieces

def encrypt(initialPermutations,ETable,keys):
    encryptedMessage = ""
    for perm in initialPermutations:
        leftRightPermutations16 = []
        L0 = ""
        R0 = ""
        for i in range(int(len(perm) / 2)): L0 += perm[i]
        for i in range(int(len(perm) / 2), int(len(perm))): R0 += perm[i]
        leftRightPermutations16.append([L0,R0])
        for i in range(1,16):
            L = leftRightPermutations16[i - 1][1]
            R = ""
            for j in range(len(leftRightPermutations16[i - 1][0])):
                R = R + "0" if leftRightPermutations16[i - 1][0][j] == fun(leftRightPermutations16[i - 1][1],keys[i],ETable)[j] else R + "1"
            leftRightPermutations16.append([L,R])

        secondLastPerm = leftRightPermutations16[15][0] + leftRightPermutations16[15][1]

        IP = [40,8,48,6,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]

        lastPerm = ""
        for num in IP:
            lastPerm += secondLastPerm[num - 1]
        encryptedMessage += lastPerm
    return encryptedMessage

def convertBinaryToInt(str):
    num = 0
    for i in range(len(str)):
        n = int(str[i])
        num += n * (2 ** (len(str) - i - 1))
    return num

def convertIntToBinary(num):
    binaryChar = ""
    while num > 0:
        binaryChar += str(num % 2)
        num = int(num / 2)
    while (len(binaryChar) < 4):
        binaryChar += "0"
    return reverseString(binaryChar)

def convertBinaryToChar(string):
    str = ""
    num = ""
    count = 0
    for i in range(len(string)):
        if count < 8:
            num += string[i]
        else:
            str += chr(convertBinaryToInt(num))
            num = ""
            i += 1
            count = 0
        count += 1
    return str

def fun(R,key,ETable):
    E = ""
    for num in ETable:
        E += R[num - 1]
    XOR = ""
    for i in range(len(key)):
        XOR = XOR + "0" if key[i] == E[i] else XOR + "1"
    groups6Bits = []
    for i in range(len(XOR)):
        group = ""
        for j in range(6):
            group += XOR[i]
        groups6Bits.append(group)
    S1 = [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
    ]
    S2 = [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
    ]
    S3 = [
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
    ]
    S4 = [
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
    ]
    S5 = [
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
    ]
    S6 = [
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
    ]
    S7 = [
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
    ]
    S8 = [
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
    ]
    groups4Bits = ""

    bin11 = groups6Bits[0][0] + groups6Bits[0][5]
    bin12 = groups6Bits[0][1] + groups6Bits[0][2] + groups6Bits[0][3] + groups6Bits[0][4]
    groups4Bits += convertIntToBinary(S1[convertBinaryToInt(bin11)][convertBinaryToInt(bin12)])

    bin21 = groups6Bits[1][0] + groups6Bits[1][5]
    bin22 = groups6Bits[1][1] + groups6Bits[1][2] + groups6Bits[1][3] + groups6Bits[1][4]
    groups4Bits += convertIntToBinary(S2[convertBinaryToInt(bin21)][convertBinaryToInt(bin22)])

    bin31 = groups6Bits[2][0] + groups6Bits[2][5]
    bin32 = groups6Bits[2][1] + groups6Bits[2][2] + groups6Bits[2][3] + groups6Bits[2][4]
    groups4Bits += convertIntToBinary(S3[convertBinaryToInt(bin31)][convertBinaryToInt(bin32)])

    bin41 = groups6Bits[3][0] + groups6Bits[3][5]
    bin42 = groups6Bits[3][1] + groups6Bits[3][2] + groups6Bits[3][3] + groups6Bits[3][4]
    groups4Bits += convertIntToBinary(S4[convertBinaryToInt(bin41)][convertBinaryToInt(bin42)])

    bin51 = groups6Bits[4][0] + groups6Bits[4][5]
    bin52 = groups6Bits[4][1] + groups6Bits[4][2] + groups6Bits[4][3] + groups6Bits[4][4]
    groups4Bits += convertIntToBinary(S5[convertBinaryToInt(bin51)][convertBinaryToInt(bin52)])

    bin61 = groups6Bits[5][0] + groups6Bits[5][5]
    bin62 = groups6Bits[5][1] + groups6Bits[5][2] + groups6Bits[5][3] + groups6Bits[5][4]
    groups4Bits += convertIntToBinary(S6[convertBinaryToInt(bin61)][convertBinaryToInt(bin62)])

    bin71 = groups6Bits[6][0] + groups6Bits[6][5]
    bin72 = groups6Bits[6][1] + groups6Bits[6][2] + groups6Bits[6][3] + groups6Bits[6][4]
    groups4Bits += convertIntToBinary(S7[convertBinaryToInt(bin71)][convertBinaryToInt(bin72)])

    bin81 = groups6Bits[7][0] + groups6Bits[7][5]
    bin82 = groups6Bits[7][1] + groups6Bits[7][2] + groups6Bits[7][3] + groups6Bits[7][4]
    groups4Bits += convertIntToBinary(S8[convertBinaryToInt(bin81)][convertBinaryToInt(bin82)])

    P = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]

    result = ""
    for num in P:
        result += groups4Bits[num - 1]
    return result




stringToConvert = input()

PC1Table = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
PC2Table = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
Shift1Table = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
IPTable = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]
ETable = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]

hexaString = convertStringToHexadecimal(stringToConvert)
for i in range(len(hexaString) % 16): hexaString += "0"
binaryString = convertHexaToBinary(hexaString)

print("Your string in hexadecimal is: " + hexaString)
print("Your hexadecimal string converted in binary is: " + binaryString)

key = randomStringGenerator()
hexaKey = convertStringToHexadecimal(key)
binaryKey = convertHexaToBinary(hexaKey)

print("Your random key string is: " + key)
print("Your key in hexadecimal is: " + hexaKey)
print("Your binary key from hexadecimal is: " + binaryKey)

keys = keysProcedures(binaryKey,PC1Table,PC2Table,Shift1Table)
splittedMessages = getSplittedMessages(binaryString)
initialPermutations = []
for message in splittedMessages: initialPermutations.append(getInitialPermutation(message,IPTable))
binaryEncryptedMessage = encrypt(initialPermutations,ETable,keys)
print("Your encrypted message is: " + binaryEncryptedMessage)


