#include <iostream>
using namespace std;

int main() {
    cout << "Menghitung total harga satu jenis barang" << endl;

    double harga_awal;
    double harga_per_item;
    int jumlah;
    double diskon;
    double diskon_total;
    double harga_setelah_diskon;
    double total;

    cout << "harga barang per item: ";
    cin >> harga_per_item;
    cout << "jumlah yang dibeli: ";
    cin >> jumlah; 

    diskon = 0.1;
    
    harga_awal = (harga_per_item * jumlah);
    diskon_total = ( harga_awal * diskon);
    total = (harga_awal - diskon_total);

    cout << "total harga barang setelah diskon: " << total << endl;
}