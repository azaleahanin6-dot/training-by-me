#include <iostream>
using namespace std;

int main() {
    int z = 20, s = 30;
    int *pz, *ps;

    pz = &z;
    ps = &s;

    cout << "Nilai Awal: " << endl;
    cout << "Z = " << z << " | S = " << s << endl;

    // Melakukan penjumlahan melalui pointer
    *pz += *ps; // setara dengan z = z + s

    cout << "\nSetelah operasi: *pz += *ps;" << endl;
    cout << "Z = " << z << endl; // Akan berubah menjadi 50
    cout << "S = " << s << endl; // Tetap 30

    return 0;
}