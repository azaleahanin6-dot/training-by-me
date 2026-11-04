#include <iostream>
using namespace std;

int main () {
    int n;

    cout << "Silahkan masukkan ukuran persegi (n): ";
    cin >> n;

    for (int i=1; i<=n; i++) {
            for (int j=1; j<=n; j++) {
               cout << "* ";
            }

            cout << endl;
    }
    return 0;
}