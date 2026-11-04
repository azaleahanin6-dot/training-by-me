#include <iostream>
using namespace std;
int main() {
    cout << "Menghitung suhu dalam satuan lain" << endl;
    double celsius;
    double kelvin;
    double fahrenheit;

    cout << "masukkan suhu dalam skala celsius: " ;
    cin >> celsius ;

    kelvin = (celsius + 273.15); 
    fahrenheit = ((celsius * 9/5) + 32);

    cout << "suhu dalam kelvin = " << kelvin << endl;
    cout << "suhu dalam fahrenheit = " << fahrenheit << endl;
    
}