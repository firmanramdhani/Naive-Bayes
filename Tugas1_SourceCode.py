import csv #untuk membaca file csv
import numpy #untuk transpose baris jadi kolom, agar mudah saat collections
import collections #untuk menghitung jumlah elemen yang sama di sebuah array

#1. MEMBACA DATA TRAIN
dataTrain = []
with open('TrainsetTugas1ML.csv') as file:
    baca = csv.reader(file,delimiter=',') #baca file dan simpan ke dalam var
    next(baca) #skip baris pertama tabel (id, age, workclass, dll)
    for d in baca:
        dataTrain.append(d[1:]) #simpan setiap data ke dalam array dari indeks 1 (age) s.d akhir (income)
        
#2. MEMECAH DATA (<=50K & >50K)
incomeKurang = []
incomeLebih = []
for d in dataTrain:
    if(d[7] == '>50K'): #d[7] adalah indeks kolom ke-7 (income)
        incomeKurang.append(d)
    else:
        incomeLebih.append(d)

###JUMLAH DATA >50K (Dalam kasus ini jumlahnya = 40)
##i = 1
##for d in incomeLebih:
##    print(i,' ',d)
##    i+=1
###JUMLAH DATA <=50K (Dalam kasus ini jumlahnya = 120)
##i = 1
##for d in incomeKurang:
##    print(i,' ',d)
##    i+=1
        
#3. MENCARI PELUANG jumlah income terhadap jumlah dataTrain
peluangLebih = len(incomeLebih)/len(dataTrain) #40/160
peluangKurang = len(incomeKurang)/len(dataTrain) #120/160

#4. MENCARI PELUANG jumlah tiap atribut terhadap jumlah income
def hitungPeluang(data):
    putar = numpy.transpose(data) #transpose array dari per baris menjadi per kolom
    hasil = []
    for d in putar:
        c = collections.Counter(d) #menghitung jumlah atribut (young=20, adult=19, <=50K=40, dst)
        for i in c:
            c[i] = c[i]/len(data) #menghitung peluang tiap atribut terhadap jumlah income (young=20/40=0.5, dst)
        hasil.append(c)
    return hasil

peluangAtributLebih = hitungPeluang(incomeLebih)
peluangAtributKurang = hitungPeluang(incomeKurang)

#5. MEMBACA DATA TEST
dataTest = []
with open('TestsetTugas1ML.csv') as file:
    baca = csv.reader(file,delimiter=',')
    next(baca)
    for d in baca:
        dataTest.append(d[1:])

#6. PENYEDERHANAAN VARIABLE
PL = peluangLebih; #40/160
PK = peluangKurang; #120/160
PaL = peluangAtributLebih #young=20/40=0.5, adult=19/40=0.475, dst
PaK = peluangAtributKurang #young=66/120=0.55, adult=53/120=0.441, dst 

#7. MENCARI KELAS (income) YANG SESUAI UNTUK DATA TEST
output = []
no = 1
for d in dataTest:
    # Menghitung peluangnya
    for i in range(0,7):
        PL = PL * PaL[i][d[i]] #PL = PL * PaL[0]['young'] = 2.38, dst
        PK = PK * PaK[i][d[i]] #PK = PK * PaK[0]['young'] = 3.36, dst
    # Mengecek mana yang lebih besar
    if(PL > PK):
        print('Kelas income data ke',no,': >50K')
        output.append('>50K')
    else:
        print('Kelas income data ke',no,': <=50K')
        output.append('<=50K')
    no+=1

#8. HASIL DISIMPAN KE DALAM CSV
with open('TebakanTugas1ML.csv', mode='w', newline='') as file:
    tulis = csv.writer(file,delimiter=',',quotechar='"')
    for d in output:
        tulis.writerow([d])


print(peluangAtributLebih);
