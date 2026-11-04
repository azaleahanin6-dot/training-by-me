#include <iostream>
#include <string>
using namespace std;

// Definisi Struct
struct DataNilai {
    string nim;
    string nama;
    int nilai;
};

int main() {
    // Array dari struct DataNilai berkapasitas 5
    DataNilai mahasiswa[5];
    int jumlahData = 0;
    char jawab;

    cout << "=== INPUT DATA MAHASISWA ===" << endl;

    // Perulangan untuk input data
    do {
        cout << "\nData ke-" << (jumlahData + 1) << endl;
        cout << "NIM   : ";
        cin >> mahasiswa[jumlahData].nim;
        cout << "Nama  : ";
        cin >> mahasiswa[jumlahData].nama;
        cout << "Nilai : ";
        cin >> mahasiswa[jumlahData].nilai;

        jumlahData++;

        if (jumlahData >= 5) {
            cout << "Kapasitas maksimum tercapai!" << endl;
            break;
        }

        cout << "Ada data lagi? (y/t): ";
        cin >> jawab;
    } while (jawab == 'y' || jawab == 'Y');

    // Menampilkan data
    cout << "\n=== DATA MAHASISWA YANG DIINPUTKAN ===" << endl;
    cout << "NIM\t\tNama\t\tNilai" << endl;
    for (int i = 0; i < jumlahData; i++) {
        cout << mahasiswa[i].nim << "\t\t"
             << mahasiswa[i].nama << "\t\t"
             << mahasiswa[i].nilai << endl;
    }

    return 0;
}