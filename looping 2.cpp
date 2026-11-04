#include <iostream>
using namespace std;

int main () {
        int angka;

        cout << "--- Program Input Angka (Input Negatif untuk Berhenti) ---" << endl;

        while (True) {
            cout << "Masukkan Angka: ";
            cin >> angka

            if (angka < 0){
                cout << "Angka negatif terdeteksi. Program dihentikan! " << endl;

                break: //Keluar dari Loop
            }
            cout << "Anda memasukkan angka: " << angka << endl;
        }
    }
