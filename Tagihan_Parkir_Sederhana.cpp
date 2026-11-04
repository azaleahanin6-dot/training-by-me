#include <iostream>
using namespace std;

int main() {
    int parkir;
    double biaya;
    cout << "===== Menghitung Tarif Parkir =====" << endl;
    cout << "Lama waktu parkir: ";
    cin >> parkir;

        if (parkir <= 2) {
            biaya = 5000;
        } else if (parkir < 9) {
            biaya = 5000 + ((parkir - 2) * 3000);
        } else {
            biaya = 25000;
        }

    cout << "Biaya parkir: Rp " << biaya << endl;
    }