#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "Masukkan jumlah data: " << endl;
    cin >> n;

    int data[n];
    for (int i = 0; i < n; i++) {
        cout << "Masukkan data ke- " << (i + 1) << ": ";
        cin >> data [i];
    }
    int maks = data [0]; // Inisialisasi dengan elemen pertama 
    for (int i = 1; i < n; i++) {
        if (data [i] > maks) {
            maks = data [i];
        }
    }
    cout << "\nData terbesar adalah: " << maks << endl;

    return 0;
} 

