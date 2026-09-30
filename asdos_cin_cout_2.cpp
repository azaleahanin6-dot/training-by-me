#include <iostream>
using namespace std;

void soal_1(){

    //soal 1//
    int panjang_sisi;
    int lebar_sisi;
    int luas_segi_empat;

    cout << "input panjang sisi: ";
    cin >> panjang_sisi ;
    cout << "input lebar sisi: ";
    cin >> lebar_sisi ;

    luas_segi_empat = (panjang_sisi * lebar_sisi);
    cout << "luas segi empat adalah " << luas_segi_empat << endl ;
} 

 void soal_2(){

    //soal 2//
    double celsius;
    double kelvin;
    double fahrenheit;

    cout << "masukkan suhu dalam skala celsius: " ;
    cin >> celsius ;

    kelvin = (celsius + 273.15); 
    fahrenheit = ((celsius * 9/5) + 32);

    cout << "suhu dalam kelvin: " << kelvin << endl;
    cout << "suhu dalam fahrenheit: " << fahrenheit << endl;
    
 }

void soal_3(){

    //soal_3//
    double phi;
    double jari_jari;
    double luas;

    phi = 3.14;

    cout << "Masukkan nilai jari jari: ";
    cin >> jari_jari;

    luas = (jari_jari * phi);
    cout << "luas ligkaran: " << luas << endl;

}

void soal_4(){

    //soal_4//
    double harga_awal;
    double harga_per_item;
    int jumlah;
    double diskon;
    double diskon_total;
    double harga_setelah_diskon;
    double total;

    cout << "harga barang per item: ";
    cin >> harga_per_item;

    cout << "jumlah yang dibeli: ";
    cin >> jumlah; 

    diskon = 0.1;
    
    harga_awal = (harga_per_item * jumlah);
    diskon_total = (jumlah * diskon);
    total = (harga_awal * diskon_total);

    cout << "total harga barang setelah diskon: " << total << endl;
 
}

void soal_5(){
 
    //soal 5//
    float jarak;
    float kecepatan;
    float estimasi_sampai;

    cout << "input jarak kota: ";
    cin >> jarak;
    cout << "input kecepatan mobil: ";
    cin >> kecepatan;

    estimasi_sampai = (jarak / kecepatan);

    cout << "estimasi waktu sampai: " << estimasi_sampai;

}

int main(){
    soal_1();
    soal_2();
    soal_3();
    soal_4();
    soal_5();
    return 0;
}








