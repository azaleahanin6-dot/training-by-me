#include <iostream>
using namespace std;

int main() {
    cout << "=== Menghitung Estimasi Pengiriman Barang ===" << endl;

    float jarak;
    float kecepatan;
    float estimasi_sampai;
    float total_jam;
    int jam;
    int menit;

    cout << "Menghitung kecepatan mobil\n";
    cout << "input jarak kota: ";
    cin >> jarak;
    cout << "input kecepatan mobil: ";
    cin >> kecepatan;

    total_jam = (jarak / kecepatan);
    jam = total_jam; 
    menit = (total_jam - jam) * 60;
    
    cout << "estimasi waktu sampai: " << jam << " jam " << menit << " menit " << endl;
}