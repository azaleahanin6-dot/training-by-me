#include <iostream>
using namespace std;

int main() {
 cout << "=== Menghitung Tarif Pengiriman ===" << endl;
 double berat;
 double jarak;
 double tarif_dasar;
 double tambahan_biaya;
 double total_biaya;

 cout << "Input Berat paket: ";
 cin >> berat;
 cout << "Input Jarak Pengiriman: ";
 cin >> jarak;

    if (berat < 3) {
        tarif_dasar = 10000;
    } else if (berat < 6) {
        tarif_dasar = 20000;
    } else if (berat < 11) {
        tarif_dasar = 35000;
    } else {
        tarif_dasar = 50000;
    }
 cout << "Tarif Dasar: Rp " << tarif_dasar << endl;

    if (jarak < 8) {
     tambahan_biaya = 0;  
    } else if (jarak < 31) {
     tambahan_biaya = 10000;
    } else if (jarak < 51) {
     tambahan_biaya = 20000;
    } else {
     tambahan_biaya = 35000;
    }
cout << "Tambahan Biaya: Rp " << tambahan_biaya << endl;

total_biaya = tarif_dasar + tambahan_biaya;
cout << "Total biaya = Rp " << total_biaya << endl;
}