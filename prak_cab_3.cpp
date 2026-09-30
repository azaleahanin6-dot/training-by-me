#include <iostream>
using namespace std;

int main() {
    int nilai;
    cout<<"Masukkan Nilai ujian (0 - 100): ";
    cin>>nilai;

    //percabangan bertingkat//
    if (nilai >= 85) {
        cout << "Grade A" << endl;
    } else if (nilai >= 70) {
        cout << "Grade B " << endl;
    } else if (nilai >= 55) {
        cout <<"Grade C" << endl;
    } else if (nilai >=40) {
        cout <<"Grade D" << endl;
    } else {
        cout <<"Grade E" << endl;
    }
    return 0;
    }