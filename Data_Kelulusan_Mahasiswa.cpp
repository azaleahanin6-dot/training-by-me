#include <iostream>
using namespace std;

int main() {
    int N;
    cout << "Input jumlah mahasiswa (N): ";
    cin >> N;

    double total_nilai = 0;
    double nilai_tertinggi = -1; // Set ke nilai paling kecil
    int jumlah_lulus = 0;
    int jumlah_gagal = 0;

    for (int i = 1; i <= N; i++) {
        double nilai;
        cout << "\nMasukkan nilai mahasiswa ke-" << i << ": ";
        cin >> nilai;

        // 1. Akumulasi Total Nilai (untuk rata-rata)
        total_nilai = total_nilai + nilai;

        // 2. Cari Nilai Tertinggi (Max)
        if (nilai > nilai_tertinggi) {
            nilai_tertinggi = nilai;
        }

        // 3. Cek Status Kelulusan & Counter
        if (nilai >= 70) {
            cout << "Status: LULUS" << endl;
            jumlah_lulus++;
        } else {
            cout << "Status: TIDAK LULUS" << endl;
            jumlah_gagal++;
        }
    }

    // 4. Hitung Rata-Rata
    double rata_rata = total_nilai / N;

    // LAPORAN AKHIR PROJECT
    cout << "\n===================================" << endl;
    cout << "--- LAPORAN EVALUASI KELAS ---" << endl;
    cout << "Rata-rata Nilai Kelas : " << rata_rata << endl;
    cout << "Nilai Tertinggi       : " << nilai_tertinggi << endl;
    cout << "Jumlah Mahasiswa Lulus: " << jumlah_lulus << endl;
    cout << "Jumlah Mahasiswa Gagal: " << jumlah_gagal << endl;

    return 0;
}