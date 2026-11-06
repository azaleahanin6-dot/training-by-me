#include <iostream>
using namespace std;
int main() {
    cout << "=== TIKET BIOSKOP ===" << endl;
    int pilihanHari, pilihanStudio;

    // input user
    cout << "Pilih Hari:\n1. Weekday\n2. Weekend\n(1/2): ";
    cin >> pilihanHari;

    switch (pilihanHari) {
    case 1: // Weekday
        cout << "Pilih Studio:\n1. Regular\n2. VIP\n(1/2): ";
        cin >> pilihanStudio;
            if (pilihanStudio == 1) {
            cout << "Harga Tiket: Rp 35.000" << endl;
            } else if (pilihanStudio == 2) {
            cout << "Harga Tiket: Rp 50.000" << endl;
            } else {
            cout << "Pilihan studio tidak valid!" << endl;
            }
    break;

    case 2: // Weekend
        cout << "Pilih Studio:\n1. Regular\n2. VIP\n(1/2): ";
        cin >> pilihanStudio;
            if (pilihanStudio == 1) {
            cout << "Harga Tiket: Rp 50.000" << endl;
            } else if (pilihanStudio == 2) {
            cout << "Harga Tiket: Rp 75.000" << endl;
            } else {
            cout << "Pilihan studio tidak valid!" << endl;
            }
    break;

    default:
        cout << "Kategori hari tidak valid!" << endl;
        break;
        }

return 0;
}