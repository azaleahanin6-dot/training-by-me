#include <iostream>
using namespace std;

// Variabel Global
const double PI = 3.14;

// Fungsi Menghitung Volume Tabung
double volumeTabung(double r, double t) {
    double volume = PI * r * r * t;
    return volume;
}

int main() {
    double r, t;
    cout << "=== MENGHITUNG VOLUME TABUNG ===" << endl;
    cout << "Masukkan jari-jari tabung : ";
    cin >> r;
    cout << "Masukkan tinggi tabung    : ";
    cin >> t;

    double hasil = volumeTabung(r, t);
    cout << "\nVolume Tabung = " << hasil << endl;

    return 0;
}