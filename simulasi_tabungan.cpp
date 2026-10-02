#include <iostream>
using namespace std;

int main() {
    double target, setoran;
    double saldo = 0;
    int bulan = 1;
    cout << "TABUNGAN\n";
    cout << "Masukkan target tabungan: ";
    cin >> target;

    while (bulan <= 24) {
        cout << "Setoran bulan ke-" << bulan << ": ";
        cin >> setoran;

        saldo = saldo + setoran;
        cout << "Saldo bulan ke-" << bulan << ": " << saldo << endl;

        // Berhenti jika target sudah tercapai
        if (saldo >= target) {
            break;
        }

        bulan = bulan + 1;
    }

    cout << "\n--- Hasil ---" << endl;
    if (saldo >= target) {
        cout << "Target berhasil dicapai dalam " << bulan << " bulan." << endl;
        cout << "Total saldo akhir: " << saldo << endl;
    } else {
        cout << "Target tidak tercapai dalam batas maksimal 24 bulan." << endl;
        cout << "Total saldo akhir: " << saldo << endl;
    }

    return 0;
}