plainText = input("Masukkan pesan yang akan di enrkipsi (64 bit): ")
print("Pesan yang akan di enkripsi: ", plainText)

# jika plaintext kurang dari 64 bit atau 8 karakter, maka tampilkan pesan error, dan program akan berhenti
if len(plainText) < 8:
    print(f"Plaintext: {plainText}, harus 64 bit atau 8 karakter")
    exit()

key = input(
    "\nMasukkan kunci untuk algoritma DES dalam bentuk hexadecimal (64 bit): ")
print("Kunci yang digunakan: ", key)

# jika kunci kurang dari 64 bit atau 16 karakter, maka tampilkan pesan error, dan program akan berhenti
if len(key) < 16:
    print(f"Kunci: {key}, harus 64 bit atau 16 karakter")
    exit()

textHexa = plainText.encode().hex().upper()
print(f"\n{plainText} dalam bentuk hexadecimal: " + textHexa)

keyUpper = key.upper()
print(f"{key} => " + keyUpper)

hxArray = {'0': "0000",
           '1': "0001",
           '2': "0010",
           '3': "0011",
           '4': "0100",
           '5': "0101",
           '6': "0110",
           '7': "0111",
           '8': "1000",
           '9': "1001",
           'A': "1010",
           'B': "1011",
           'C': "1100",
           'D': "1101",
           'E': "1110",
           'F': "1111"}

bin = ""
for i in range(len(textHexa)):
    bin = bin + hxArray[textHexa[i]]

splitText = ' '.join([bin[i:i+8] for i in range(0, len(bin), 8)])

# ini adalah tabel permutasi awal
initPerm = [58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7]

permutation = ""
for i in range(0, 64):
    permutation = permutation + bin[initPerm[i] - 1]

split = ' '.join([permutation[i:i+8] for i in range(0, len(permutation), 8)])
print("\nIP: " + split)

# Splitting
left = permutation[0:32]
right = permutation[32:64]

kiri = ' '.join([left[i:i+8] for i in range(0, len(left), 8)])
print("\nL0: " + kiri)

kanan = ' '.join([right[i:i+8] for i in range(0, len(right), 8)])
print("R0: " + kanan)

binkey = ""
for i in range(len(keyUpper)):
    binkey = binkey + hxArray[keyUpper[i]]

split = ' '.join([binkey[i:i+8] for i in range(0, len(binkey), 8)])
print("\nK: " + split)

# ini adalah tabel pc1
pc1 = [57, 49, 41, 33, 25, 17, 9, 1,
       58, 50, 42, 34, 26, 18, 10, 2,
       59, 51, 43, 35, 27, 19, 11, 3,
       60, 52, 44, 36, 63, 55, 47, 39,
       31, 23, 15, 7, 62, 54, 46, 38,
       30, 22, 14, 6, 61, 53, 45, 37,
       29, 21, 13, 5, 28, 20, 12, 4]

permutationkey = ""
for i in range(0, 56):
    permutationkey = permutationkey + binkey[pc1[i] - 1]

separated_text = ' '.join([permutationkey[i:i+8]
                          for i in range(0, len(permutationkey), 8)])
print("\nK+: " + separated_text)

left1 = permutationkey[0:28]
right1 = permutationkey[28:56]

kiri1 = ' '.join([left1[i:i+7] for i in range(0, len(left1), 7)])
print("\nC0: " + kiri1)

kanan1 = ' '.join([right1[i:i+7] for i in range(0, len(right1), 7)])
print("D0: " + kanan1)

# ini adalah tabel shift key
shift_table = [1, 1, 2, 2,
               2, 2, 2, 2,
               1, 2, 2, 2,
               2, 2, 2, 1]

for i in range(0, 16):
    pergeseranKunciKiri = ""  # inisialisasi pergeseran kunci
    for j in range(shift_table[i]):
        for k in range(1, len(left1)):
            pergeseranKunciKiri = pergeseranKunciKiri + left1[k]
        pergeseranKunciKiri = pergeseranKunciKiri + left1[0]
        left1 = pergeseranKunciKiri
        pergeseranKunciKiri = ""

    pergeseranKunciKanan = ""
    for j in range(shift_table[i]):
        for k in range(1, len(right1)):
            pergeseranKunciKanan = pergeseranKunciKanan + right1[k]
        pergeseranKunciKanan = pergeseranKunciKanan + right1[0]
        right1 = pergeseranKunciKanan
        pergeseranKunciKanan = ""

    print(f"\nC{i+1} =", left1)
    print(f"D{i+1} =", right1)


def shift_left(k, geser):
    s = ""  # inisialisasi pergeseran kunci
    for i in range(geser):
        for j in range(1, len(k)):
            s = s + k[j]
        s = s + k[0]
        k = s
        s = ""
    return k


for i in range(0, 16):
    # memanggil fungsi shift left, untuk melakukan pergeseran bit pada leftKey sesuai nilai dalam shift_table
    leftkey = shift_left(left1, shift_table[i])
    # memanggil fungsi shift left, untuk melakukan pergeseran bit pada rightKey sesuai nilai dalam shift_table
    rightkey = shift_left(right1, shift_table[i])

    left1 = leftkey  # mengganti nilai left1 dengan leftkey
    right1 = rightkey  # mengganti nilai right1 dengan rightkey

    combine_str = left1 + right1  # menggabungkan left1 dan right1
    # memisahkan string menjadi 8 bit
    split = ' '.join([combine_str[i:i+8]
                     for i in range(0, len(combine_str), 8)])

# ini adalah tabel pc2
pc2 = [14, 17, 11, 24, 1, 5, 3, 28,
       15, 6, 21, 10, 23, 19, 12, 4,
       26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40,
       51, 45, 33, 48, 44, 49, 39, 56,
       34, 53, 46, 42, 50, 36, 29, 32]

keyPC2 = []

for i in range(0, 16):
    leftkey = shift_left(left1, shift_table[i])
    rightkey = shift_left(right1, shift_table[i])

    left1 = leftkey
    right1 = rightkey

    combine_str = left1 + right1  # menggabungkan left1 dan right1

    round_key = ""  # inisialisasi round key
    for j in range(0, 48):
        round_key = round_key + combine_str[pc2[j] - 1]

    # memisahkan string menjadi 6 bit
    split = ' '.join([round_key[i:i+6] for i in range(0, len(round_key), 6)])

    print(f"\nK{i+1} = ", split)

    keyPC2.append(round_key)  # menambahkan round_key ke dalam array keyPC2

ekspansiArray = [32, 1, 2, 3, 4, 5, 4, 5,
                 6, 7, 8, 9, 8, 9, 10, 11,
                 12, 13, 12, 13, 14, 15, 16, 17,
                 16, 17, 18, 19, 20, 21, 20, 21,
                 22, 23, 24, 25, 24, 25, 26, 27,
                 28, 29, 28, 29, 30, 31, 32, 1]

SboxArray = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
              [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
              [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
              [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

             [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
              [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
              [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
              [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

             [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
              [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
              [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
              [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

             [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
              [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
              [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
              [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

             [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
              [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
              [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
              [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

             [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
              [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
              [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
              [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

             [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
              [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
              [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
              [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

             [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
              [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
              [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
              [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

PboxArray = [16, 7, 20, 21,
             29, 12, 28, 17,
             1, 15, 23, 26,
             5, 18, 31, 10,
             2, 8, 24, 14,
             32, 27, 3, 9,
             19, 13, 30, 6,
             22, 11, 4, 25]

inversPerArray = [40, 8, 48, 16, 56, 24, 64, 32,
                  39, 7, 47, 15, 55, 23, 63, 31,
                  38, 6, 46, 14, 54, 22, 62, 30,
                  37, 5, 45, 13, 53, 21, 61, 29,
                  36, 4, 44, 12, 52, 20, 60, 28,
                  35, 3, 43, 11, 51, 19, 59, 27,
                  34, 2, 42, 10, 50, 18, 58, 26,
                  33, 1, 41, 9, 49, 17, 57, 25]

ekspansi = ""  # inisialisasi ekspansi
for i in range(16):  # putaaran sebanyak 16 kali
    permutation = ""  # inisialisasi permutasi untuk memasukkan nilai ekspansi
    for j in range(0, 48):
        # melakukan ekspansi oada kunci kanan, menggunakan tabel ekspansi
        permutation = permutation + right[ekspansiArray[j] - 1]
    ekspansi = permutation

    print(f"\nEkspansi (R{i+1}): ", ekspansi)

    xor = ""  # inisialisasi xor
    for j in range(48):
        # memeriksa apakah nilai ekspansi sama dengan nilai keyPC2 menggunakan index i dan j
        if ekspansi[j] == keyPC2[i][j]:
            xor = xor + "0"  # jika kondisi diatas terpenuhi, maka tambahkan nilai 0 ke dalam variabel xor
        else:
            xor = xor + "1"  # jika kondisi diatas tidak terpenuhi, maka tambahkan nilai 1 ke dalam variabel xor
    print("XOR: ", xor)

    sbox = ""  # inisialisasi sbox
    for j in range(0, 8):  # melakukan operasi sbox sebanyak 8 kali
        # mengambil 2 bit pertama dan dua bit terakhir dari blok xor untuk mendapatkan index baris pada S-box
        row = int(xor[j * 6] + xor[j * 6 + 5], 2)
        # mengambil 4 bit tengah dari blok xor untuk mendapatkan index kolom pada S-box
        col = int(xor[j * 6 + 1:j * 6 + 5], 2)
        # mengambil nilai dari S-box menggunakan index row dan col
        val = SboxArray[j][row][col]
        # mengubah nilai val menjadi biner dengan 4 bit, dan menambahkan nilai val ke dalam variabel sbox
        sbox = sbox + format(val, '04b')

    print("Sbox:", sbox)

    pbox = ""  # inisialisasi pbox
    for j in range(32):
        # mengambil elemen dari sbox menggunakan index dari PBoxArray dan menambahkan nilai ke dalam variabel pbox
        pbox = pbox + sbox[PboxArray[j] - 1]

    print("Pbox:", pbox)

    inversing = ""  # inisialisasi inversing
    for j in range(32):
        if left[j] == pbox[j]:  # memeriksa apakah nilai left sama dengan nilai pbox menggunakan index j
            # jika kondisi diatas terpenuhi, maka tambahkan nilai 0 ke dalam variabel inversing
            inversing = inversing + "0"
        else:
            # jika kondisi diatas tidak terpenuhi, maka tambahkan nilai 1 ke dalam variabel inversing
            inversing = inversing + "1"
    left = inversing

    if i != 15:  # memeriksa apakah ini bukan putaran terakhir
        # menampilkan nilai kunci kiri yang akan digunakan sebagai acuan untuk ke kunci kanan pada putaran selanjutnya
        print(f"L{i+1}", f"to R{i+1} :", left)
        # menampilkan nilai kunci kanan yang akan digunakan sebagai acuan untuk ke kunci kiri pada putaran selanjutnya
        print(f"R{i+1}", f"to L{i+1} :", right)
    else:
        # jika sudah mencaai putaran terakhir, maka tampilkan nilai kunci kiri
        print(f"L{i+1}:", left)
        # jika sudah mencaai putaran terakhir, maka tampilkan nilai kunci kanan
        print(f"R{i+1}:", right)

    if i != 15:  # memeriksa apakah ini bukan putaran terakhir
        # jika kondisi diatas terpenuhi, maka tukar nilai left dan right
        left, right = right, left
    print(f"Round {i+1} |", f"L{i+1}:", left, f"R{i+1}:", right)

combine = left + right  # menggabungkan left dan right
print("\nCombine R16 dan L16:", combine)

cipher_text = ""  # inisialisasi cipher text
for j in range(64):
    # mengambil elemen dari combine menggunakan index dari inversPerArray dan menambahkan nilai ke dalam variabel cipher_text
    cipher_text = cipher_text + combine[inversPerArray[j] - 1]

print("\nCipher Text:", cipher_text)

# digunakan untuk membalikkan array dari keyPC2 dan sebagai penggunaan dekripsi, lalu disimpan dalam variabel invKeyPC2
invKeyPC2 = keyPC2[::-1]

separated_text = ' '.join([cipher_text[i:i+8]
                          for i in range(0, len(cipher_text), 8)])

permutation = ""
for i in range(0, 64):
    permutation = permutation + cipher_text[initPerm[i] - 1]

separated_text = ' '.join([permutation[i:i+8]
                          for i in range(0, len(permutation), 8)])

left = permutation[0:32]
right = permutation[32:64]

kiri = ' '.join([left[i:i+8] for i in range(0, len(left), 8)])

kanan = ' '.join([right[i:i+8] for i in range(0, len(right), 8)])

ekspansi = ""  # inisialisasi ekspansi
for i in range(16):  # putaaran sebanyak 16 kali
    permutation = ""  # inisialisasi permutasi untuk memasukkan nilai ekspansi
    for j in range(0, 48):
        # melakukan ekspansi oada kunci kanan, menggunakan tabel ekspansi
        permutation = permutation + right[ekspansiArray[j] - 1]
    ekspansi = permutation

    print(f"\nEkspansi (R{i+1}): ", ekspansi)

    xor = ""  # inisialisasi xor
    for j in range(48):
        # memeriksa apakah nilai ekspansi sama dengan nilai keyPC2 menggunakan index i dan j
        if ekspansi[j] == invKeyPC2[i][j]:
            xor = xor + "0"  # jika kondisi diatas terpenuhi, maka tambahkan nilai 0 ke dalam variabel xor
        else:
            xor = xor + "1"  # jika kondisi diatas tidak terpenuhi, maka tambahkan nilai 1 ke dalam variabel xor
    print("XOR: ", xor)

    sbox = ""  # inisialisasi sbox
    for j in range(0, 8):  # melakukan operasi sbox sebanyak 8 kali
        # mengambil 2 bit pertama dan dua bit terakhir dari blok xor untuk mendapatkan index baris pada S-box
        row = int(xor[j * 6] + xor[j * 6 + 5], 2)
        # mengambil 4 bit tengah dari blok xor untuk mendapatkan index kolom pada S-box
        col = int(xor[j * 6 + 1:j * 6 + 5], 2)
        # mengambil nilai dari S-box menggunakan index row dan col
        val = SboxArray[j][row][col]
        # mengubah nilai val menjadi biner dengan 4 bit, dan menambahkan nilai val ke dalam variabel sbox
        sbox = sbox + format(val, '04b')

    print("Sbox:", sbox)

    pbox = ""  # inisialisasi pbox
    for j in range(32):
        # mengambil elemen dari sbox menggunakan index dari PBoxArray dan menambahkan nilai ke dalam variabel pbox
        pbox = pbox + sbox[PboxArray[j] - 1]

    print("Pbox:", pbox)

    inversing = ""  # inisialisasi inversing
    for j in range(32):
        if left[j] == pbox[j]:  # memeriksa apakah nilai left sama dengan nilai pbox menggunakan index i dan j
            # jika kondisi diatas terpenuhi, maka tambahkan nilai 0 ke dalam variabel inversing
            inversing = inversing + "0"
        else:
            # jika kondisi diatas tidak terpenuhi, maka tambahkan nilai 1 ke dalam variabel inversing
            inversing = inversing + "1"
    left = inversing

    # menampilkan nilai kunci kiri yang akan digunakan sebagai acuan untuk ke kunci kanan pada putaran selanjutnya
    print(f"L{i+1}", f"| to R{i+1} :", left)
    # menampilkan nilai kunci kanan yang akan digunakan sebagai acuan untuk ke kunci kiri pada putaran selanjutnya
    print(f"R{i+1}", f"| to L{i+1} :", right)

    if i != 15:  # memeriksa apakah ini bukan putaran terakhir
        # jika kondisi diatas terpenuhi, maka tukar nilai left dan right
        left, right = right, left
    print(f"Round {i+1} |", f"L{i+1}:", left, f"R{i+1}:", right)

combine = left + right  # menggabungkan left dan right
print("\nCombine R16 dan L16:", combine)

decrypt_text = ""
for j in range(64):  # melakukan invers permutasi
    # melakukan invers permutasi dengan menggunakan tabel inversPer yang telah ditentukan
    decrypt_text = decrypt_text + combine[inversPerArray[j] - 1]

print("\nDekripsi (binary format):", decrypt_text)

separated_text = ' '.join([decrypt_text[i:i+8]
                          for i in range(0, len(decrypt_text), 8)])

binary_chunks = separated_text.split()  # memisahkan biner menjadi 8 bit

# mengubah biner menjadi integer, lalu mengonversi integer menjadi karakter unicode, kemudian menggabungkan karakter unicode menjadi string
text = ''.join(chr(int(chunk, 2)) for chunk in binary_chunks)

print("\nDekripsi:", text)
