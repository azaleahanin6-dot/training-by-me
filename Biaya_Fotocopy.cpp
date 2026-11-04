#include <iostream>
using namespace std;

int main (){
    cout << "=== Penghitungan total biaya fotokopi anda ===" << endl;
    char status_pelanggan;
    float jumlah_kertas;
    float harga_per_lembar;
    float total_biaya;

    // Input status pelanggan 
    cout << "Apakah anda pelanggan? (Y/T): ";
    cin >> status_pelanggan;
    cout << "Input jumlah kertas: ";
    cin >> jumlah_kertas;

    // Menentukan harga per lembar 
        if (status_pelanggan == 'Y' || status_pelanggan == 'y') {
            harga_per_lembar = 75;
        } else if (status_pelanggan == 'T' || status_pelanggan == 't') {
            if (jumlah_kertas < 100)
            harga_per_lembar = 150;
            else if (jumlah_kertas < 200)
            harga_per_lembar = 100;
            else 
            harga_per_lembar = 80;
        } else {
            cout << "Jawaban tidak valid" << endl;
        }

    // Menghitung total biaya 
    total_biaya = harga_per_lembar * jumlah_kertas; 
    cout << "Harga per lembar: Rp " << harga_per_lembar << endl;
    cout << "Biaya yang harus anda bayar: " << total_biaya << endl;

    }