#include <iostream>
using namespace std;

    int main() {
    int umur;
    char statusSehat; // 'Y' atau 'T'
    
    cout << "Cek kelayakan pembuatan SIM\n";
    cout << "Masukkan Umur Anda: ";
    cin >> umur;
    cout << "Apakah Anda sehat secara fisik & mental? (Y/T): ";
    cin >> statusSehat;
    // Penggunaan operator logika AND (&&)
    if (umur >= 17 && (statusSehat == 'Y' || statusSehat == 'y')) {
    cout << "Status: Anda LAYAK untuk membuat SIM." << endl;
    } else {
    cout << "Status: Anda BELUM LAYAK untuk membuat SIM." << endl;
    }
    return 0;
    }