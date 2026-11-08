#include <iostream>
using namespace std;

int main() {
    cout << "=== BIAYA PARKIR ===" << endl;
    
    int N;
    double total_pendapatan = 0;

    cout << "Input jumlah kendaraan (N): ";
    cin >> N;

    for (int i = 1; i <= N; i++) {
        int jenis_kendaraan;
        int durasi_jam;
        double biaya = 0;

        cout << "\n--- Kendaraan " << i << " ---" << endl;
        cout << "Jenis Kendaraan:\n1: Motor\n2: Mobil\n(1/2): ";
        cin >> jenis_kendaraan;
        cout << "Durasi Parkir (jam): ";
        cin >> durasi_jam;

        if (jenis_kendaraan == 1) { // MOTOR
            if (durasi_jam <= 2) {
                biaya = durasi_jam * 3000;
            } else {
                biaya = (2 * 3000) + ((durasi_jam - 2) * 2000);
            }
            cout << "Biaya parkir motor: Rp" << biaya << endl;
        } 
        else if (jenis_kendaraan == 2) { // MOBIL
            if (durasi_jam <= 2) {
                biaya = durasi_jam * 6000;
            } else {
                biaya = (2 * 6000) + ((durasi_jam - 2) * 4000);
            }
            cout << "Biaya parkir mobil: Rp" << biaya << endl;
        } 
        else {
            cout << "Jenis kendaraan salah" << endl;
            biaya = 0;
        }

        // Akumulasi total pendapatan parkir
        total_pendapatan = total_pendapatan + biaya;
    }

    cout << "\n===================================" << endl;
    cout << "Total pendapatan parkir hari ini: Rp" << total_pendapatan << endl;

    return 0;
}