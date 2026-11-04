#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    cout << "=== Perkembangbiakan Bakteri ===" << endl;

    int bakteri; 
    int jam_maks;

    cout << "Input bakteri awal: ";
    cin >> bakteri;
    cout << "Input jam maks: ";
    cin >> jam_maks;

    for (int jam = 1; jam <= jam_maks; jam++) {
        int bakteri_lahir = bakteri / 2;
        int bakteri_mati = bakteri / 5;

        // Update populasi bakteri untuk jam berikutnya
        bakteri = bakteri + bakteri_lahir - bakteri_mati;

        cout << "Jam ke-" << jam << ":" << endl;
        cout << "- Lahir: " << bakteri_lahir << endl;
        cout << "- Mati: " << bakteri_mati << endl;
        cout << "- Total populasi: " << bakteri << endl << endl;
    }

    return 0;
}