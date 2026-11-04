#include <iostream>
using namespace std;

int main() {
    int nilai [5];

    // Mengisi nilai elemen array
    nilai[0] = 80;
    nilai[1] = 70;
    nilai[2] = 82;
    nilai[3] = 90;
    nilai[4] = 77;

    cout << "Daftar Nilai Mahasiswa: " << endl;
    for (int i = 0; i < 5; i++) {
        cout << "Nilai Indeks ke-" << i << " = " << nilai [i] << endl;
    }
 return 0;
}
