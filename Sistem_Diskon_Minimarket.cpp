#include <iostream>
using namespace std;

int main() {

    // SISTEM HITUNG DISKON KASIR MINIMARKET //
    cout << "=====SISTEM HITUNG DISKON KASIR MINIMARKET=====\n" ;

    string nama;
    double total_pembelian;
    double diskon;
    string bonus;
    double bill;

    // input nama dan total pembelian //
    cout << "Masukkan nama anda: " ;
    cin >> nama ;
    cout << "Masukkan total pembelian anda: " ;
    cin >> total_pembelian ;

    // syarat pemberian diskon dan bonus //
        if (total_pembelian >= 500000) {
           diskon = (total_pembelian * 0.2) ;
           bill = (total_pembelian - diskon);
        } else if (total_pembelian >= 200000) {
            diskon = (total_pembelian * 0.1) ;
            bill = (total_pembelian - diskon);
        } else {
            diskon = 0;
            bill = (total_pembelian - diskon);
        }
    // tampilkan output //
    cout << "Selamat datang " << nama << "!!!" << endl;
    cout << "Total pembelian anda = " << total_pembelian << endl;
    if (total_pembelian >= 200000) {
        cout << "Diskon anda = " << diskon << endl;
    }
    cout << "Tagihan yang harus anda bayar = " << bill << endl;
    if (total_pembelian >= 500000) {
        cout << "Anda mendapat bonus voucher belanja senilai Rp 50000" << endl;
    }
}