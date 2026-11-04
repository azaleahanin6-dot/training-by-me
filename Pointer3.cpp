#include <iostream>
using namespace std;

// Deklarasi Struct
struct Kartesian {
    double x;
    double y;
};

int main() {
    Kartesian k1; // Membuat variabel k1 bertipe struct Kartesian

    cout << "Masukkan nilai X: ";
    cin >> k1.x;
    cout << "Masukkan nilai Y: ";
    cin >> k1.y;

    cout << "\nTitik Koordinat Kartesian yang dimasukkan: (" << k1.x << ", " << k1.y << ")" << endl;

    return 0;
}