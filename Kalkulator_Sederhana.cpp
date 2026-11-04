#include <iostream>
#include <cmath>
using namespace std;

int main (){
    cout << "=== Kalkulator sederhana ===" << endl;
    float bilangan_pertama;
    float bilangan_kedua;
    string pilihan;
    float hasil_operasi;

    // Input bilangan 
    cout << "Input bilangan pertama: ";
    cin >> bilangan_pertama;
    cout << "Input bilangan kedua: ";
    cin >> bilangan_kedua;

    // Menampilkan menu operasi 
    cout << "Operasi Matematika" << endl;
    cout << "1. Penjumlahan" << endl;
    cout << "2. Pengurangan" << endl;
    cout << "3. Perkalian" << endl;
    cout << "4. Pembagian" << endl;
    cout << "Masukkan pilihan anda: ";
    cin >> pilihan;

    // Pengoperasian input bilangan 
        if (pilihan == "1") {
            cout << "Hasil = " << (bilangan_pertama + bilangan_kedua) << endl;
        } else if (pilihan == "2") {
            cout << "Hasil = " << (bilangan_pertama - bilangan_kedua) << endl;
        } else if (pilihan == "3") {
            cout << "Hasil = " << (bilangan_pertama * bilangan_kedua) << endl;
        } else if (pilihan == "4") {
            cout << "Hasil = " << (bilangan_pertama / bilangan_kedua) << endl;
        } else {
            cout << "Pilihan tidak valid" << endl;
            return;
        }

    }