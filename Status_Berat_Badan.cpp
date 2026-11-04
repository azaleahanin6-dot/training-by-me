#include <iostream>
using namespace std;

    void program_1(){

    //soal 1//
    cout << "=== Program Penilai Status Berat Badan ===" << endl;

        float tinggi_badan;
        float berat_badan;
        int status_berat;

        // Input data user
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

    void program_2(){

    //soal 2//
    cout << "===== Penentu Gemuk atau Kurus =====" << endl;

    int tinggi;
    int berat;

    cout << "Tinggi badan: ";
    cin >> tinggi;
    cout << "Berat Badan: ";
    cin >> berat;

        if (tinggi - berat < 100) {
            cout << "Gemuk" ;
        } else if (tinggi - berat < 110) {
            cout << "Ideal";
        } else if (tinggi - berat < 120) {
            cout << "Kurus";
        } else {
            cout << "Terlalu Kurus";
        }
}

void program_3(){

    //soal 3//
    cout << "=== Program pengecek status IMT ===\n";

    float IMT;

    //Input data user
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

    int main(){
    program_1();
    program_2();
    program_3();
    return 0;
}