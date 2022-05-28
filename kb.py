#Nama   : Rachman Ardiansyah Harahap
#NIM    : 1910114017666
#Kelas  : 06TPLE025 

#Fuzzy Sugeno
#Studi Kasus : carwash

#Kecepatan mesin air : min 500 rpm dan max 1200 rpm.
#Banyaknya mobil  : sedikit 40 dan banyak 80.
#Tingkat Kebersihan  : rendah 40, sedang 50, dan 60 tinggi.

def down(x, xmin, xmax):
    return (xmax- x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class mobil():
    minimum = 40
    maximum = 80

    def sedikit(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def banyak(self, x):
        if x <= self.minimum:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.minimum, self.maximum)

class bersih():
    minimum = 40
    medium = 50
    maximum = 60

    def rendah(self, x):
        if x >= self.medium:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.medium)
    
    def sedang(self, x):
        if self.minimum < x < self.medium:
            return up(x, self.minimum, self.medium)
        elif self.medium < x < self.maximum:
            return down(x, self.medium, self.maximum)
        elif x == self.medium:
            return 1
        else:
            return 0

    def tinggi(self, x):
        if x <= self.medium:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.medium, self.maximum)

class mesinair():
    minimum = 500
    maximum = 1200
    
    def lambat(self, α):
        if α >= self.maximum:
            return 0
        elif α <= self.minimum:
            return 1

    def cepat(self, α):
        if α <= self.minimum:
            return 0
        elif α >= self.maximum:
            return 1

    # 2 permintaan 3 persediaan
    def inferensi(self, jumlah_mobil, jumlah_bersih):
        mbl = mobil()
        brs = bersih()
        result = []
        
        # [R1] Jika mobil SEDIKIT, dan mobil RENDAH, 
        #     MAKA mesinair = 500
        α1 = min(mbl.sedikit(jumlah_mobil),brs.rendah(jumlah_bersih))
        z1 = self.minimum
        result.append((α1, z1))

        # [R2] Jika mobil SEDIKIT, dan bersih SEDANG, 
        #     MAKA mesinair = 10 * jumlah_bersih + 100
        α2 = min(mbl.sedikit(jumlah_mobil), brs.sedang(jumlah_bersih))
        z2 = 10 * jumlah_bersih + 200
        result.append((α2, z2))

        # [R3] Jika mobil SEDIKIT, dan bersih TINGGI, 
        #     MAKA mesinair = 10 * jumlah_bersih + 200
        α3 = min(mbl.sedikit(jumlah_mobil), brs.tinggi(jumlah_bersih))
        z3 = 10 * jumlah_bersih + 300
        result.append((α3, z3))

        # [R4] Jika mobil BANYAK, dan bersih RENDAH,
        #     MAKA mesinair = 5 * jumlah_mobil + 2 * jumlah_bersih
        α4 = min(mbl.banyak(jumlah_mobil), brs.rendah(jumlah_bersih))
        z4 = 5 * jumlah_mobil + 2 * jumlah_bersih
        result.append((α4, z4))

        # [R5] Jika mobil BANYAK, dan bersih SEDANG,
        #     MAKA mesinair = 5 * jumlah_mobil + 4 * jumlah_bersih + 100
        α5 = min(mbl.banyak(jumlah_mobil), brs.sedang(jumlah_bersih))
        z5 = 5 * jumlah_mobil + 4 * jumlah_bersih + 300
        result.append((α5, z5))

        # [R6] Jika mobil BANYAK, dan bersih TINGGI,
        #     MAKA mesinair = 5 * jumlah_mobil + 5 * jumlah_bersih + 300
        α6 = min(mbl.banyak(jumlah_mobil), brs.tinggi(jumlah_bersih))
        z6 = 5 * jumlah_mobil + 5 * jumlah_bersih + 200
        result.append((α6, z6))

        return result
    
    def defuzifikasi(self, jumlah_mobil, jumlah_bersih):
        inferensi_values = self.inferensi(jumlah_mobil, jumlah_bersih)
        return sum([(value[0]* value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])