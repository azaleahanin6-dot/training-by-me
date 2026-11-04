#include <iostream>
using namespace std;

    void cara_1(){

    //soal 1//
    cout << "=== Hasil Nilai Ujian ===" << endl;
    int nilai;

    // Input Nilai
    cout <<"Masukkan Nilai ujian (0 - 100): ";
    cin >> nilai;

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
    }

    void cara_2(){

    //soal 2//
    cout << "=== Hasil Nilai Akhir ===" << endl;
    int nilai_UTS = 90;
    int nilai_UAS = 85;
    int nilai_tugas = 90;

    double hasil = (nilai_UTS * 0.3) + (nilai_UAS * 0.4) + (nilai_tugas * 0.3);
    cout << hasil << endl;

    }
    int main(){
    cara_1();
    cara_2();
    return 0;
}
