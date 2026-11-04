#include <iostream>
using namespace std;

int main() {

    // SISTEM SELEKSI BEASISWA MAHASISWA //
    cout << "===== SISTEM SELEKSI BEASISWA MAHASISWA =====\n" ;

    double IPK ;
    double gaji ;

    // INPUT DATA MAHASISWA //
    cout << "Masukkan nilai IPK anda : " ;
    cin >> IPK ;

    // PENGECEKAN NILAI IPK DAN PENDAPATAN ORANG TUA //
        if (IPK < 1 || IPK > 4) {
            cout << "IPK tidak valid" << endl;
        } else if (IPK < 3.25 ) {
            cout << "Gagal Seleksi: Nilai IPK dibawah standar minimum (3.25)." ;
        } else {
            cout << "Masukkan pendapatan orang tua anda : " ;
            cin >> gaji ;
                if (gaji <= 0) {
                    cout << "Pendapatan tidak valid." << endl;
                } else if (gaji < 3000000) {
                    cout << "Selamat, Anda Lolos Beasiswa Penuh (100%)." << endl;
                } else if (gaji >= 3000000 && gaji <= 5000000) {    
                    cout << "Selamat, Anda Lolos Beasiswa Parsial (50%)." << endl;
                } else {
                    cout << "Gagal Seleksi: Pendapatan Orang Tua Melebihi Batas Maksimal Kuota." << endl;
                }
        }
return 0;
}