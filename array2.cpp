#include <iostream>
using namespace std;

int main() {
 int n;
 float total = 0, rataRata;

 cout << "Masukkan jumlah data: ";
 cin >> n;

 float nilai[n];

 for (int i = 0; i< n; i++) {
    cout << "Masukkan Nilai ke-" << (i + 1) << ": ";
    cin >> nilai [i];
    total += nilai [i];
 }
 rataRata = total / n;

 cout << "\n=======" << endl;
 cout << "Total Nilai = " << total << endl;
 cout << "Nilai Rata-rata = " << rataRata << endl;

 return 0;
} 
