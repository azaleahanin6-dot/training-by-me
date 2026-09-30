#include <iostream>
using namespace std;

    int main() {
        int n;
        long long faktorial = 1;

        cout << "Masukkan angka untuk faktorial (n): ";
        cin << n;

        if (n < 0) {
            cout << "Faktorial total didefinisikan untuk bilangan negatif! " << endl;"
        } else {
         cout << n << "! = ";
         for (int i = n; i >= 1; i--) {
         faktorial *= i;
         cout << i;
         if (i > 1) cout << " x "
         }         }
    }