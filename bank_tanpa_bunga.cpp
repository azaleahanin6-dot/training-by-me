#include <iostream>
using namespace std;

int main() {

    cout << "==== Bank Tanpa Bunga ====" << endl;
    
    double tabungan;
    double persen_bonus;
    double target_tabungan;
    int tahun_tercapai = 0; // Penanda tahun pertama kali target tembus

    //input data user
    cout << "Input tabungan awal: ";
    cin >> tabungan;
    cout << "Input persen bonus tahunan (%): ";
    cin >> persen_bonus;
    cout << "Input target tabungan: ";
    cin >> target_tabungan;

    for (int tahun = 1; tahun <= 100; tahun++) {
        // 1. Tambah bonus tahunan
        tabungan = tabungan + (tabungan * persen_bonus / 100);

        // 2. Hitung potongan biaya admin berdasarkan saldo saat itu
        if (tabungan > 50000000) {
            tabungan = tabungan - (tabungan * 0.02); // Potong 2%
        } else {
            tabungan = tabungan - (tabungan * 0.01); // Potong 1%
        }

        // 3. Cek apakah target pertama kali tercapai
        if (tabungan >= target_tabungan && tahun_tercapai == 0) {
            tahun_tercapai = tahun;
        }
    }

    // Output Hasil Akhir
    cout << "\n-----------------------------------" << endl;
    if (tahun_tercapai > 0) {
        cout << "Target tabungan pertama kali tercapai pada tahun ke-" << tahun_tercapai << endl;
    } else {
        cout << "Target gagal dicapai dalam batas waktu 100 tahun." << endl;
    }

    return 0;
}