#include <iostream>
using namespace std;

void soal_5() {
    // soal 5 //
    // Program penghitung total tagihan listrik pelanggan (Nested IF) //

    double kwh;
    string golongan;
    char status_subsidi;
    double biaya_listrik = 0;
    double potongan_subsidi = 0;
    double biaya_admin = 0;
    double total_tagihan_listrik = 0;

    // Input data pelanggan //
    cout << "Masukkan golongan anda (R1 / R2 / B1): ";
    cin >> golongan;

    cout << "Input jumlah pemakaian listrik (dalam kWh): ";
    cin >> kwh;

    cout << "Status subsidi (Y / N): ";
    cin >> status_subsidi;

    // IF Luar: Cek Golongan //
    if (golongan == "R1" || golongan == "r1") {

        // IF Dalam: Hitung pemakaian bertingkat untuk R1 //
        if (kwh <= 100) {
            biaya_listrik = kwh * 1500;
        } else if (kwh <= 300) {
            biaya_listrik = (100 * 1500) + ((kwh - 100) * 2000);
        } else {
            biaya_listrik = (100 * 1500) + (200 * 2000) + ((kwh - 300) * 2500);
        }

    } else if (golongan == "R2" || golongan == "r2") {

        // IF Dalam: Hitung pemakaian bertingkat untuk R2 //
        if (kwh <= 100) {
            biaya_listrik = kwh * 1800;
        } else if (kwh <= 300) {
            biaya_listrik = (100 * 1800) + ((kwh - 100) * 2300);
        } else {
            biaya_listrik = (100 * 1800) + (200 * 2300) + ((kwh - 300) * 2800);
        }

    } else if (golongan == "B1" || golongan == "b1") {

        // IF Dalam: Hitung pemakaian bertingkat untuk B1 //
        if (kwh <= 100) {
            biaya_listrik = kwh * 2000;
        } else if (kwh <= 300) {
            biaya_listrik = (100 * 2000) + ((kwh - 100) * 2500);
        } else {
            biaya_listrik = (100 * 2000) + (200 * 2500) + ((kwh - 300) * 3000);
        }

    } else {
        cout << "Golongan tidak valid!" << endl;
        return;
    }

    // IF Luar: Cek Status Subsidi //
    if (status_subsidi == 'Y' || status_subsidi == 'y') {
        
        // IF Dalam: Cek persen potongan berdasarkan kWh //
        if (kwh <= 300) {
            potongan_subsidi = 0.20 * biaya_listrik;
        } else {
            potongan_subsidi = 0.10 * biaya_listrik;
        }
    }

    // Cek Biaya Administrasi //
    if (kwh > 500) {
        biaya_admin = 10000;
    }

    // Hitung Total Pembayaran //
    total_tagihan_listrik = biaya_listrik - potongan_subsidi + biaya_admin;

    // Output Rincian //
    cout << "\n--- Rincian Tagihan Listrik ---" << endl;
    cout << "Biaya Listrik Kotor : Rp " << biaya_listrik << endl;
    cout << "Potongan Subsidi    : Rp " << potongan_subsidi << endl;
    cout << "Biaya Administrasi  : Rp " << biaya_admin << endl;
    cout << "Total Tagihan       : Rp " << total_tagihan_listrik << endl;
}
int main ()
{
    
}