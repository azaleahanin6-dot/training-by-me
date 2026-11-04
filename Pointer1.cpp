#include <iostream>
using namespace std;

int main() {
    int x = 87;
    int y;
    int *px; // Deklarasi variabel pointer px

    px = &x; // px diberi nilai berupa alamat dari x
    y = *px; // y disalin dari nilai yang ditunjuk px (yaitu x)

    cout << "--- PENGAMATAN POINTER ---" << endl;
    cout << "Alamat memori x (&x)          = " << &x << endl;
    cout << "Isi variabel px (alamat x)    = " << px << endl;
    cout << "Nilai x mula-mula            = " << x << endl;
    cout << "Nilai yang ditunjuk (*px)     = " << *px << endl;
    cout << "Nilai y                       = " << y << endl;

    // Mengubah nilai x melalui pointer px
    *px = 100;
    cout << "\nSetelah eksekusi: *px = 100;" << endl;
    cout << "Isi variabel x sekarang = " << x << endl;

    return 0;
}