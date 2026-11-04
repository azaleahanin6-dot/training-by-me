#include <iostream>
using namespace std;

    void bangun_1(){

    //soal 1//
    cout << "Menghitung luas segi empat\n";
    int panjang_sisi;
    int lebar_sisi;
    int luas_segi_empat;

    cout << "input panjang sisi: ";
    cin >> panjang_sisi ;
    cout << "input lebar sisi: ";
    cin >> lebar_sisi ;

    luas_segi_empat = (panjang_sisi * lebar_sisi);
    cout << "luas segi empat = " << luas_segi_empat << endl ;
    } 

    void bangun_2(){

    //soal 2//
    cout << "Menghitung luas lingkaran\n";
    double phi;
    double jari_jari;
    double luas;

    phi = 3.14;

    cout << "Masukkan nilai jari jari: ";
    cin >> jari_jari;

    luas = (jari_jari * phi);
    cout << "luas ligkaran: " << luas << endl;

    }
    int main(){
    bangun_1();
    bangun_2();
    return 0;
}




    