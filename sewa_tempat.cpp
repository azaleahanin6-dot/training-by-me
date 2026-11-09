#include <iostream>
using namespace std;

int main() {
    // program pembayaran sewa tempat
    cout << "PROGRAM PENYEWAAN TEMPAT" << endl;
    int N;
    double total_pendapatan = 0;

    cout << "Input jumlah pemesan (N): ";
    cin >> N;

    for (int i = 1; i <= N; i++) {
        int jenis_lapangan;
        double durasi_sewa;
        double tarif_per_jam = 0;
        double persen_diskon = 0;
        double total_bayar = 0;

        cout << "\n--- Pemesan " << i << " ---" << endl;
        cout << "Jenis Lapangan (1: Futsal, 2: Badminton): ";
        cin >> jenis_lapangan;
        cout << "Durasi Sewa (jam): ";
        cin >> durasi_sewa;

        // 1. Tentukan Tarif & Diskon
        if (jenis_lapangan == 1) { // FUTSAL
            tarif_per_jam = 100000;
            if (durasi_sewa > 3) {
                persen_diskon = 0.10; // 10%
            }
        } 
        else if (jenis_lapangan == 2) { // BADMINTON
            tarif_per_jam = 50000;
            if (durasi_sewa > 3) {
                persen_diskon = 0.05; // 5%
            }
        } 
        else {
            cout << "Jenis lapangan tidak valid" << endl;
            tarif_per_jam = 0;
        }

        // 2. Hitung Total Bayar
        if (tarif_per_jam > 0) {
            double kotor = durasi_sewa * tarif_per_jam;
            double potongan = kotor * persen_diskon;
            total_bayar = kotor - potongan;
        }

        cout << "Total bayar pemesan " << i << ": Rp" << total_bayar << endl;

        // 3. Akumulasi Total Pendapatan
        total_pendapatan = total_pendapatan + total_bayar;
    }

    // Output Akhir
    cout << "\n===================================" << endl;
    cout << "Total seluruh pendapatan sewa: Rp" << total_pendapatan << endl;

    return 0;
}