#include <iostream>
#include <iomanip>
using namespace std;

    int main (){
    cout << "=== Penghitung total tagihan listrik ===" << endl;
    double kWh;
    string golongan;
    char status_subsidi;
    double biaya_listrik;
    double potongan_subsidi;
    double biaya_admin = 0;
    double total_tagihan_listrik;
    
    // Input data pelanggan 
    cout << "Masukkan golongan anda (R1 / R2 / B1) : ";
    cin >> golongan;

    cout << "Input jumlah pemakaian listrik (dalam kWh): ";
    cin >> kWh;

    cout << "status subsidi (Y / N) : ";
    cin >> status_subsidi;

    // Menghitung tarif listrik 
         if (golongan == "R1"||golongan == "r1") {
            if (kWh <= 100) {
                biaya_listrik = kWh * 1500;
            } else if (kWh <= 300) {
                biaya_listrik = (100 * 1500) + ((kWh - 100) * 2000);
            } else {
                biaya_listrik = (100 * 1500) + (300 * 2000) + ((kWh - 300) * 2500);
            }   
        } else if (golongan == "R2"||golongan == "r2") {
            if (kWh <= 100) {
                biaya_listrik = kWh * 1800;
            } else if (kWh <= 300) {
                biaya_listrik = (100 * 1800) + ((kWh - 100) * 2300);
            } else {
                biaya_listrik = (100 * 1800) + (300 * 2300) + ((kWh - 300) * 2800);
            }
        } else if (golongan == "B1"||golongan == "b1") {
            if (kWh <= 100) {
                biaya_listrik = kWh * 2000;
            } else if (kWh <= 300) {
                biaya_listrik = (100 * 2000) + ((kWh - 100) * 2500);
            } else {
                biaya_listrik = (100 * 2000) + (200 * 2500) + ((kWh - 300) * 3000);
            }
        } else {
            cout << "Golongan tidak valid!" << endl;
        }

    // Cek Status Subsidi 
        if (status_subsidi == 'Y'||status_subsidi =='y') {
            if (kWh <= 300) {
                potongan_subsidi = 0.20 * biaya_listrik;
            } else {
                potongan_subsidi = 0;
            }
        } else if (status_subsidi == 'N'|| status_subsidi == 'n') {
            potongan_subsidi = 0;
        } else {
            cout << "status subsidi tidak valid" << endl;
        }

    // Cek Biaya Administrasi 
    if (kWh > 500) {
        biaya_admin = 10000;
    }

    // Hitung Total Pembayaran //
    total_tagihan_listrik = biaya_listrik - potongan_subsidi + biaya_admin;
    cout << fixed << setprecision(0);

    // Rincian //
    cout << "Rincian Tagihan Listrik" << endl;
    cout << "Biaya Listrik Kotor : Rp " << biaya_listrik << endl;
    cout << "Potongan Subsidi    : Rp " << potongan_subsidi << endl;
    cout << "Biaya Administrasi  : Rp " << biaya_admin << endl;
    cout << "Total Tagihan       : Rp " << total_tagihan_listrik << endl;
    }
