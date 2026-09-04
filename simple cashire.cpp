#include <iostream>
using namespace std;

int main(){

cout<< "MY STORE" << endl;
    double harga_buku;
    int jumlah_buku;
    double total_harga;
    double diskon;
    double harga_final;

    cout << "Masukkan harga buku: ";
    cin >> harga_buku ;
    cout << "Masukkan jumlah buku: ";
    cin >> jumlah_buku ;

 total_harga = (harga_buku * jumlah_buku);
 cout << "jumlah uang yang harus dibayar: " << total_harga << endl;

    if (total_harga > 100000){
        diskon = total_harga * 0.1;
        harga_final = total_harga - diskon;
        cout << "selamat! anda mendapat diskon sebesar 10%." << endl;
        cout << "harga final yang harus anda bayar: " << harga_final << endl;
    } else {
        diskon = 0;
        harga_final = total_harga;
        cout << "tidak ada potongan harga ya kak!" << endl;
        cout << "harga final yang harus anda bayar: " << harga_final << endl;
    }

return 0;
}