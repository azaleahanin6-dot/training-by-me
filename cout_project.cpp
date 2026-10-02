#include <iostream>
using namespace std;

    void soal_1(){

    //soal 1//
    int panjang_sisi;
    int lebar_sisi;
    int luas_segi_empat;

    cout << "Menghitung luas segi empat\n";
    cout << "input panjang sisi: ";
    cin >> panjang_sisi ;
    cout << "input lebar sisi: ";
    cin >> lebar_sisi ;

    luas_segi_empat = (panjang_sisi * lebar_sisi);
    cout << "luas segi empat = " << luas_segi_empat << endl ;
    } 

    void soal_2(){

    //soal 2//
    double celsius;
    double kelvin;
    double fahrenheit;

    cout << "Menghitung suhu dalam satuan lain\n";
    cout << "masukkan suhu dalam skala celsius: " ;
    cin >> celsius ;

    kelvin = (celsius + 273.15); 
    fahrenheit = ((celsius * 9/5) + 32);

    cout << "suhu dalam kelvin = " << kelvin << endl;
    cout << "suhu dalam fahrenheit = " << fahrenheit << endl;
    
    }

    void soal_3(){

    //soal_3//
    double phi;
    double jari_jari;
    double luas;

    phi = 3.14;

    cout << "Menghitung luas lingkaran\n";
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

    cout << "Menghitung total harga satu jenis barang\n";
    cout << "harga barang per item: ";
    cin >> harga_per_item;

    cout << "jumlah yang dibeli: ";
    cin >> jumlah; 

    diskon = 0.1;
    
    harga_awal = (harga_per_item * jumlah);
    diskon_total = ( harga_awal * diskon);
    total = (harga_awal - diskon_total);

    cout << "total harga barang setelah diskon: " << total << endl;
 
    }

    void soal_5(){
 
    //soal 5//
    float jarak;
    float kecepatan;
    float estimasi_sampai;
    float total_jam;
    int jam;
    int menit;

    cout << "Menghitung kecepatan mobil\n";
    cout << "input jarak kota: ";
    cin >> jarak;
    cout << "input kecepatan mobil: ";
    cin >> kecepatan;

    total_jam = (jarak / kecepatan);
    jam = total_jam; 
    menit = (total_jam - jam) * 60;
    
    cout << "estimasi waktu sampai: " << jam << " jam " << menit << " menit " << endl;

    }

    void soal_6(){

    //soal 6//
    string nama = "Azalea";
    int umur = 18;
    float tinggi_badan = 157;
    bool apakah_sudah_menikah = 0;

    cout << "Mencetak identitas diri\n";
    cout << " nama : " << nama << endl;
    cout << " umur : " << umur << endl;
    cout << " tinggi badan : " << tinggi_badan << endl;
    cout << " apakah sudah menikah : " << apakah_sudah_menikah << endl;

    }

    void soal_7(){
    
    //soal 7//
    int nilai_UTS = 90;
    int nilai_UAS = 85;
    int nilai_tugas = 90;

    double hasil = (nilai_UTS * 0.3) + (nilai_UAS * 0.4) + (nilai_tugas * 0.3);
    cout << hasil << endl;

    }

int main(){
    soal_1();
    soal_2();
    soal_3();
    soal_4();
    soal_5();
    soal_6();
    soal_7();
    return 0;
}








