#include <iostream>
#include <cmath>
using namespace std;

void Uji_Pemahaman(){

    // soal uji pemahaman //
    float IMT;

    cout << "Program mengecek status IMT ";
    cout << "Input your IMT: ";
    cin >> IMT;

    if (IMT < 18.5) {
    cout<< "Kurus" << endl;
    } else if (IMT < 25.0) {
    cout << "Normal" << endl;
    } else if (IMT < 30.0) {
    cout << "Gemuk" << endl;
    } else {
    cout << "Obesitas" << endl;
    }

}

void soal_1(){

    // soal 1 //
    // Menentukan apakah seseorang terlalu gemuk atau kurus //

    float tinggi_badan;
    float berat_badan;
    int status_berat;

    // input tinggi badan dan berat badan //
    cout << "Input tinggi badan: ";
    cin >> tinggi_badan;
    cout << "Input berat badan: ";
    cin >> berat_badan;
    // Menghitung status berat seseorang //
    status_berat = (tinggi_badan - berat_badan);

    if (status_berat > 120) {
    cout << "Sangat Kurus" << endl;
    } else if (status_berat > 111) {
    cout << "Kurus" << endl;
    } else if (status_berat > 100) {
    cout << "Ideal" << endl; 
    } else {
    cout << "Kegemukan" << endl;
    }

}

void soal_2(){

    // soal 2 //
    // menentukan total biaya fotokopi //

    string status_pelanggan;
    float jumlah_kertas;
    float harga_per_lembar;
    float total_biaya;

    // Input status pelanggan //
    cout << "Apakah anda pelanggan? (Jawab : YA atau TIDAK): ";
    cin >> status_pelanggan;

    // Input jumlah kertas //
    cout << "Input jumlah kertas: ";
    cin >> jumlah_kertas;

    // Menentukan harga per lembar //
    if (status_pelanggan == "YA" || status_pelanggan == "ya") {
        harga_per_lembar = 75;
    } else if (status_pelanggan == "TIDAK" || status_pelanggan == "tidak") {
        if (jumlah_kertas < 100)
        harga_per_lembar = 150;
        else if (jumlah_kertas < 200)
        harga_per_lembar = 100;
        else 
        harga_per_lembar = 80;
    } else {
        cout << "Jawaban tidak valid" << endl;
        return;
    }

    // Menghitung total biaya // 
    total_biaya = harga_per_lembar * jumlah_kertas; 
    cout << "Harga per lembar: Rp " << harga_per_lembar << endl;
    cout << "Biaya yang harus anda bayar: " << total_biaya << endl;

}

void soal_3(){

    // tugas 3 //
    // Kalkulator sederhana //

    float bilangan_pertama;
    float bilangan_kedua;
    string pilihan;
    float hasil_operasi;

    // Input bilangan //
    cout << "Input bilangan pertama: ";
    cin >> bilangan_pertama;
    cout << "Input bilangan kedua: ";
    cin >> bilangan_kedua;

    // Menampilkan menu operasi //
    cout << "Operasi Matematika" << endl;
    cout << "1. Penjumlahan" << endl;
    cout << "2. Pengurangan" << endl;
    cout << "3. Perkalian" << endl;
    cout << "4. Pembagian" << endl;
    cout << "Masukkan pilihan anda: ";
    cin >> pilihan;

    // Pengoperasian input bilangan //
    if (pilihan == "1. Penjumlahan") {
        cout << "Hasil = " << (bilangan_pertama + bilangan_kedua) << endl;
    } else if (pilihan == "2. Pengurangan") {
        cout << "Hasil = " << (bilangan_pertama - bilangan_kedua) << endl;
    } else if (pilihan == "3. Perkalian") {
        cout << "Hasil = " << (bilangan_pertama * bilangan_kedua) << endl;
    } else if (pilihan == "4. Pembagian") {
        cout << "Hasil = " << (bilangan_pertama / bilangan_kedua) << endl;
    } else {
        cout << "Pilihan tidak valid" << endl;
        return;
    }

}

void soal_4(){

    // tugas 4 //
    // Menghitung ukuran sebuah bangun //

     char pilihan;
     float panjang_sisi_kubus;
     float volume_kubus;
     float panjang_jari_jari_lingkaran;
     float luas_lingkaran;
     float tinggi_silinder;
     float volume_silinder;

    // Menampilkan menu //
    cout << "Menu Penghitungan: " << endl;
    cout << "(1) menghitung volume kubus " << endl;
    cout << "(2) Menghitung luas lingkaran " << endl;
    cout << "(3) Menghitung volume silinder" << endl;
    cout << "Input angkanya saja (1, 2, atau 3)" << endl;

    // Input pilihan //
    cout << "Masukkan pilihan anda: ";
    cin >> pilihan;

    // proses penghitungan //
    switch (pilihan) {
    case 1 :
        cout << "Input panjang sisi kubus: ";
        cin >> panjang_sisi_kubus;
        volume_kubus = pow(panjang_sisi_kubus, 3);
        cout << "volume kubus = " << volume_kubus << endl;
        break;
    case 2 :
        cout << "Input panjang jari jari lingkaran: ";
        cin >> panjang_jari_jari_lingkaran;
        luas_lingkaran = (3.14 * panjang_jari_jari_lingkaran);
        cout << "Luas lingkaran = " << luas_lingkaran << endl;
        break;
    case 3 :
        cout << "Input panjang jari jari lingkaran: ";
        cin >> panjang_jari_jari_lingkaran;
        cout << "Input tinggi silinder: ";
        cin >> tinggi_silinder;
        volume_silinder = (3.14 * panjang_jari_jari_lingkaran * tinggi_silinder);
        cout << "Volume silinder = " << volume_silinder << endl;
        break;
    default: 
        cout << "Pilihan tidak valid" << endl;
        break;
    }
}

void soal_5(){

    // soal 5 //
    // Program penghitung total tagihan listrik pelanggan //

    double kWh;
    string golongan;
    char status_subsidi;
    double biaya_listrik;
    double potongan_subsidi;
    double biaya_admin;
    double total_tagihan_listrik;
    

    // Input data pelanggan //
    cout << "Masukkan golongan anda: (R1 / R2 / B1)";
    cin >> golongan;

    cout << "Input jumlah pemakaian listrik (dalam kWh): ";
    cin >> kWh;

    cout << "status subsidi (Y / N) : ";
    cin >> status_subsidi;

    // Menghitung tarif listrik //
    
    if (golongan == "R1") {
        if (kWh <= 100) {
            biaya_listrik = kWh * 1500;
        } else if (kWh <= 300) {
            biaya_listrik = (100 * 1500) + ((kWh - 100) * 2000);
        } else {
            biaya_listrik = (100 * 1500) + (200 * 2000) + ((kWh - 300) * 2500);
        }   
    } else if (golongan == "R2") {
        if (kWh <= 100) {
            biaya_listrik = kWh * 1800;
        } else if (kWh <= 300) {
            biaya_listrik = (100 * 1800) + ((kWh - 100) * 2300);
        } else {
            biaya_listrik = (100 * 1800) + (200 * 2300) + ((kWh - 300) * 2800);
        }
    } else if (golongan == "B1"){
        if (kWh <= 100) {
            biaya_listrik = kWh * 2000;
        } else if (kWh <= 300) {
            biaya_listrik = (100 * 2000) + ((kWh - 100) * 2500);
        } else {
            biaya_listrik = (100 * 2000) + (200 * 2500) + ((kWh - 300) * 3000);
        }
    } else {
        cout << "Golongan tidak valid!" << endl;
        return;
    }

    // Cek Status Subsidi //
    if (status_subsidi == 'Y') {
        if (kWh <= 300) {
            potongan_subsidi = 0.20 * biaya_listrik;
        } else {
            potongan_subsidi = 0.10 * biaya_listrik;
        }
    }

    // Cek Biaya Administrasi //
    if (kWh > 500) {
        biaya_admin = 10000;
    }

    // Hitung Total Pembayaran //
    total_tagihan_listrik = biaya_listrik - potongan_subsidi + biaya_admin;

    // Rincian //
    cout << "Rincian Tagihan Listrik" << endl;
    cout << "Biaya Listrik Kotor : Rp " << biaya_listrik << endl;
    cout << "Potongan Subsidi    : Rp " << potongan_subsidi << endl;
    cout << "Biaya Administrasi  : Rp " << biaya_admin << endl;
    cout << "Total Tagihan       : Rp " << total_tagihan_listrik << endl;
}

int main() {
    Uji_Pemahaman ();
    soal_1 ();
    soal_2 ();
    soal_3 ();
    soal_4 ();
    soal_5 ();
    return 0;
}
