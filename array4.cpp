#include <iostream>
using namespace std;

// Prototype Prosedur
void membuatSegitiga(int tinggi);

int main() {
    int n;
    cout << "=== MEMBUAT SEGITIGA TERBALIK ===" << endl;

    cout << "Masukkan tinggi segitiga : ";
    cin >> n;
    cout << endl;

    // Pemanggilan Prosedur
    membuatSegitiga(n);

    return 0;
}

// Definisi Prosedur
void membuatSegitiga(int tinggi) {
    for (int i = 0; i < tinggi; i++) {
        // Loop 1: Cetak spasi
        for (int j = 0; j < i; j++) {
            cout << " ";
        }
        // Loop 2: Cetak bintang
        for (int j = 0; j < (2 * (tinggi - i) - 1); j++) {
            cout << "*";
        }
        cout << endl;
    }
}