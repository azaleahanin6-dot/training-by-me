#include <iostream>
using namespace std;

int main() {
    int N;
    double total_omset = 0;

    cout << "Input jumlah meja (N): ";
    cin >> N;

    for (int meja = 1; meja <= N; meja++) {
        char kategori_member;
        double total_belanja;
        double persentase_diskon = 0;

        cout << "\n--- Meja " << meja << " ---" << endl;
        cout << "Kategori Member (V/M/N): ";
        cin >> kategori_member;
        cout << "Total Belanja (Rp): ";
        cin >> total_belanja;

        // Percabangan Bertingkat Diskon
        if (kategori_member == 'V' || kategori_member == 'v') {
            if (total_belanja > 500000) {
                persentase_diskon = 0.20; // 20%
            } else {
                persentase_diskon = 0.15; // 15%
            }
        } else if (kategori_member == 'M' || kategori_member == 'm') {
            if (total_belanja > 500000) {
                persentase_diskon = 0.10; // 10%
            } else {
                persentase_diskon = 0.05; // 5%
            }
        } else if (kategori_member == 'N' || kategori_member == 'n') {
            persentase_diskon = 0.0; // 0%
        } else {
            cout << "Kategori tidak valid" << endl;
            persentase_diskon = 0.0;
        }

        // Hitung total bayar meja ini
        double total_bayar = total_belanja - (total_belanja * persentase_diskon);
        cout << "Total bayar meja " << meja << ": Rp" << total_bayar << endl;

        // Akumulasi total omset harian
        total_omset = total_omset + total_bayar;
    }

    // Hasil Akhir
    cout << "\n===================================" << endl;
    cout << "Total seluruh omset pendapatan: Rp" << total_omset << endl;

    return 0;
}