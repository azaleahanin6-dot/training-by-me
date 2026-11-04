#include <iostream>
#include <iomanip>
using namespace std;

int main() {

    // SISTEM TABUNGAN IMPIAN //
    cout << "===== TABUNGAN IMPIAN =====" << endl;

    double target;
    double setoran;
    double saldo = 0;
    int bulan;
    int hari = 1;

    // Input Target Tabungan Akhir //
    cout << "Masukkan target tabungan: ";
    cin >> target;

    while (hari <= 24) {
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