#include <iostream>
using namespace std;

int main() {
    int n;

    cout << "Rekap nilai mahasiswa\n";
    cout << "Masukkan jumlah mahasiswa: ";
    cin >> n;

    int i = 1;
    double total = 0;
    double max = 0;
    double min = 100;
    int lulus = 0;
    int tidak_lulus = 0;

    while (i <= n) {
        double nilai;
        cout << "Nilai mahasiswa ke-" << i << ": ";
        cin >> nilai;

        total = total + nilai;

        if (nilai > max) max = nilai;
        if (nilai < min) min = nilai;

        if (nilai >= 60) {
            lulus = lulus + 1;
        } else {
            tidak_lulus = tidak_lulus + 1;
        }

        i = i + 1;
    }

    cout << "\nRata-rata: " << total / n << endl;
    cout << "Nilai tertinggi: " << max << endl;
    cout << "Nilai terendah: " << min << endl;
    cout << "Jumlah lulus: " << lulus << endl;
    cout << "Jumlah tidak lulus: " << tidak_lulus << endl;

    return 0;
}