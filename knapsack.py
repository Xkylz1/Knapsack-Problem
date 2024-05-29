import random

# Konstanta
KAP_KNAPSACK = 25  # Kapasitas knapsack
BANYAK_ITEM = 10  # Jumlah item
ITEM_KNAPSACK = [
    ("Barang 1", 3, 2),
    ("Barang 2", 7, 2),
    ("Barang 3", 4, 1),
    ("Barang 4", 2, 3),
    ("Barang 5", 5, 4),
    ("Barang 6", 6, 3),
    ("Barang 7", 1, 5),
    ("Barang 8", 8, 1),
    ("Barang 9", 3, 6),
    ("Barang 10", 4, 2)
]

UK_GRUP = 5  # Ukuran grup untuk seleksi
UK_POP = 20  # Ukuran populasi
PERS_ELIT = 10  # Persentase elit
PROB_CROSSOVER = 0.7  # Probabilitas crossover
PROB_MUTASI = 0.1  # Probabilitas mutasi
MAX_GEN_STABIL = 50  # Maksimum generasi stabil
MAX_BANYAK_GEN = 1000  # Maksimum jumlah generasi

def hitungFitness(krom):
    fitness = 0.0
    total_bobot = 0.0
    for i, (item, bobot, profit) in enumerate(ITEM_KNAPSACK):
        if krom[i] == 1:
            fitness += float(profit)
            total_bobot += float(bobot)
        if total_bobot > KAP_KNAPSACK:
            return 0
    return fitness

def perbaikiKromosom(pop):
    for krom in pop:
        while hitungFitness(krom) == 0:
            # ubah bit ‘1’ menjadi ‘0’
            bit_1 = [i for i, bit in enumerate(krom) if bit == 1]
            krom[random.choice(bit_1)] = 0

def solusiTerbaik(pop):
    fitness_tertinggi, krom_terbaik = max(((hitungFitness(krom), krom) for krom in pop), key=lambda x: x[0])
    # print(f"Fitness tertinggi: {fitness_tertinggi}")
    # print(f"Kromosom terbaik: {krom_terbaik}")

    item_terpilih, bobot_item, profit_item = [], [], []
    for i, (_, bobot, profit) in enumerate(ITEM_KNAPSACK):
        if krom_terbaik[i] == 1:
            item_terpilih.append(ITEM_KNAPSACK[i][0])  # Add the item name
            bobot_item.append(bobot)
            profit_item.append(profit)
    # print(f"Item terpilih: {item_terpilih}")
    # print(f"Bobot item: {bobot_item}")
    # print(f"Profit item: {profit_item}")

    return krom_terbaik, fitness_tertinggi, item_terpilih, bobot_item, profit_item




def seleksi(pop):
    # Grup dengan n kromosom
    grup_krom = random.sample(pop, UK_GRUP)
    fitness_krom_terpilih, krom_terpilih = max(((hitungFitness(krom), krom) for krom in grup_krom), key=lambda x: x[0])
    return krom_terpilih

def crossover(krom1, krom2):
    # Pilih titik potong penyilangan acak
    tipot = random.randint(1, BANYAK_ITEM - 1)
    # Bentuk kromosom baru
    krom_anak1 = krom1[:tipot] + krom2[tipot:]
    krom_anak2 = krom2[:tipot] + krom1[tipot:]
    return krom_anak1, krom_anak2

def mutasi(krom):
    # Inversi bit terpilih
    bit_mut = random.randint(0, BANYAK_ITEM - 1)
    krom[bit_mut] = int(not krom[bit_mut])
    # Perbaiki kromosom hasil mutasi
    while hitungFitness(krom) == 0:
        # Ubah bit ‘1’ menjadi ‘0’
        bit_1 = [i for i, bit in enumerate(krom) if bit == 1]
        krom[random.choice(bit_1)] = 0

def bentukPopulasiBaru(pop):
    # Banyaknya kromosom elit
    krom_elit = int(UK_POP * PERS_ELIT / 100)
    # Urutkan populasi berdasarkan fitness
    pop_terurut = [krom for fitness, krom in sorted(((hitungFitness(krom), krom) for krom in pop), reverse=True)]
    # Menambahkan kromosom elit ke dalam populasi baru
    pop_baru = pop_terurut[:krom_elit]
    # Sisa populasi dibentuk dari hasil penyilangan dan mutasi
    while len(pop_baru) < UK_POP:
        # Seleksi induk kromosom yg akan disilangkan
        induk1 = seleksi(pop)
        induk2 = seleksi(pop)
        # Silangkan sesuai prob. crossover
        if random.random() < PROB_CROSSOVER:
            anak_krom1, anak_krom2 = crossover(induk1, induk2)
        else:
            anak_krom1, anak_krom2 = induk1, induk2
        # Mutasi anak kromosom berdasarkan prob. mutasi
        if random.random() < PROB_MUTASI:
            mutasi(anak_krom1)
        if random.random() < PROB_MUTASI:
            mutasi(anak_krom2)
        # Tambahkan kromosom ke dalam populasi baru
        pop_baru.append(anak_krom1)
        pop_baru.append(anak_krom2)
    return pop_baru[:UK_POP]

# Inisialisasi
populasi = [[random.randint(0, 1) for _ in range(BANYAK_ITEM)] for _ in range(UK_POP)]
generasi = 0
generasi_stabil = 0
fitness_tertinggi = 0
krom_terbaik = []
item_terpilih, bobot_item, profit_item = [], [], []

while True:
    populasi = bentukPopulasiBaru(populasi)
    generasi += 1
    
    # Evaluasi populasi baru untuk mendapatkan solusi terbaik
    krom_terbaik_baru, fitness_tertinggi_baru, item_terpilih_baru, bobot_item_baru, profit_item_baru = solusiTerbaik(populasi)
    
    print(f"Generasi {generasi}")
    print(f"Fitness tertinggi baru: {fitness_tertinggi_baru}")
    
    if fitness_tertinggi_baru != fitness_tertinggi:
        # Solusi yang lebih baik ditemukan
        krom_terbaik = krom_terbaik_baru
        fitness_tertinggi = fitness_tertinggi_baru
        item_terpilih = item_terpilih_baru
        bobot_item = bobot_item_baru
        profit_item = profit_item_baru
        generasi_stabil = 0
        print("Solusi baru ditemukan, generasi stabil direset.")
    else:
        generasi_stabil += 1
        print("Tidak ada solusi baru, generasi stabil bertambah.")
    
    # Cek kondisi berhenti
    if generasi_stabil >= MAX_GEN_STABIL:
        # Fitness tertinggi tidak berubah setelah MAX_GEN_STABIL generasi => hentikan proses
        print("Generasi stabil tercapai.")
        break
    if generasi >= MAX_BANYAK_GEN:
        # Maksimum generasi tercapai => hentikan proses
        print("Max generasi tercapai.")
        break

# Output hasil terbaik
print(f"Jumlah generasi: {generasi}")
print(f"Kromosom terbaik: {krom_terbaik}")
print(f"Fitness tertinggi: {fitness_tertinggi}")
print(f"Item terpilih: {item_terpilih}")
print(f"Bobot item: {bobot_item}")
print(f"Profit item: {profit_item}")
