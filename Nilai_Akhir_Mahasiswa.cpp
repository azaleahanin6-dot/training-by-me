#include <iostream>
using namespace std;

int main() {
    cout << "===== Menghitung Nilai Akhir =====" << endl;
    double tugas, kuis, UTS, UAS, projek, nilai_akhir;
    char huruf;

    cout << "Input nilai tugas: ";
    cin >> tugas ;
        tugas = (tugas * 0.15);
    cout << "Input nilai kuis: ";
    cin >> kuis;
        kuis = (kuis * 0.10);
    cout << "Input nilai UTS: ";
    cin >> UTS;
        UTS = (UTS * 0.25);
    cout << "Input nilai UAS: ";
    cin >> UAS;
     UAS = (UAS * 0.25);
    cout << "Input nilai projek: ";
    cin >> projek;
     projek = (projek * 0.25);
    
     nilai_akhir = (tugas + kuis + UTS + UAS + projek);
     cout << "Nilai akhir anda: " << nilai_akhir << endl;

        if (nilai_akhir >= 86) {
            huruf = 'A' ;
        } else if (nilai_akhir >= 81) {
            huruf = 'AB';
        } else if (nilai_akhir >= 71) {
            huruf = 'B';
        } else if (nilai_akhir >= 66) {
            huruf = 'BC';
        } else if (nilai_akhir >= 61) {
            huruf = 'C';
        } else if (nilai_akhir >= 56) {
            huruf = 'CD';
        } else if (nilai_akhir >= 51) {
            huruf = 'D';
        } else {
            huruf = 'E';
        }
        
    cout << "nilai_anda: " << huruf << endl;

    }