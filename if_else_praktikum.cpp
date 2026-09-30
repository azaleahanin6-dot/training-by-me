#include <iostream>
using namespace std;

int main() {
int nilai;
cout<<"Masukkan Nilai ujian (0 - 100): ";
cin>>nilai;

if (nilai >= 60) {
    cout << "Selamat! anda dinyatakan LULUS " << endl;
} else {
    cout << "Maaf anda tidak lulus " << endl;
}

return 0;
}