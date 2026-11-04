#include <iostream>
#include <cmath>
using namespace std;
    int main() {
    cout << "=== Penghitungan ukuran sebuah bangun ===" << endl;
    int pilihan;
    float panjang_sisi_kubus;
    float volume_kubus;
    float panjang_jari_jari_lingkaran;
    float luas_lingkaran;
    float tinggi_silinder;
    float volume_silinder;

    // Menampilkan menu 
    cout << "=== Penghitungan ukuran sebuah bangun ===\n";
    cout << "Menu Penghitungan: " << endl;
    cout << "(1) menghitung volume kubus " << endl;
    cout << "(2) Menghitung luas lingkaran " << endl;
    cout << "(3) Menghitung volume silinder" << endl;

    // Input pilihan 
    cout << "Masukkan pilihan anda: ";
    cin >> pilihan;

    // proses penghitungan 
        switch (pilihan) {
        case 1 :
            cout << "Input panjang sisi kubus: ";
            cin >> panjang_sisi_kubus;
            volume_kubus = pow(panjang_sisi_kubus, 3);
            cout << "volume kubus = " << volume_kubus << endl;
            break;
        case 2 :
            cout << "Input panjang jari jari lingkaran: ";
            cin >> panjang_jari_jari_lingkaran;
            luas_lingkaran = (3.14 * panjang_jari_jari_lingkaran);
            cout << "Luas lingkaran = " << luas_lingkaran << endl;
            break;
        case 3 :
            cout << "Input panjang jari jari lingkaran: ";
            cin >> panjang_jari_jari_lingkaran;
            cout << "Input tinggi silinder: ";
            cin >> tinggi_silinder;
            volume_silinder = (3.14 * panjang_jari_jari_lingkaran * tinggi_silinder);
            cout << "Volume silinder = " << volume_silinder << endl;
            break;
        default: 
            cout << "Pilihan tidak valid" << endl;
            break;
        }
    }

