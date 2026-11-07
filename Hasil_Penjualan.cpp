#include <iostream>
using namespace std;

int main() {
    cout << "=== Data Penjualan ===" << endl;
    int jumlahHari = 7;
    double pendapatan [jumlahHari];
    double total = 0;
    double rataRata;
    double tertinggi = 0;
    int hariMelebihi1Juta = 0;

    for (int i = 0; i < jumlahHari; i++) {
        cout << "Masukkan pendapatan hari ke-" << i + 1 << ": Rp ";
        cin >> pendapatan[i];
        total += pendapatan[i];

        if (pendapatan[i] > tertinggi) {
            tertinggi = pendapatan[i];
        }

        if (pendapatan[i] > 1000000) {
            hariMelebihi1Juta++;
        }
    }

    rataRata = total / jumlahHari;

    cout << "\n=== Hasil Analisis Penjualan ===" << endl;
    cout << "Total pendapatan selama 7 hari: Rp " << total << endl;
    cout << "Rata-rata pendapatan per hari : Rp " << rataRata << endl;
    cout << "Pendapatan tertinggi          : Rp " << tertinggi << endl;
    cout << "Jumlah hari pendapatan > Rp1.000.000: " << hariMelebihi1Juta << " hari" << endl;

    return 0;
}