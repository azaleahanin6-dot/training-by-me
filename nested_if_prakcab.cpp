#include <iostream>
#include <string>
using namespace std;

    int main() {
    string username;
    string password;

    cout << "=== SISTEM LOGIN ===" << endl;
    cout << "Username: ";
    cin >> username;
    cout << "Password: ";
    cin >> password;
    // Nested If (If di dalam If)
    if (username == "admin") {
    if (password == "admin123") {
    cout << "Login BERHASIL! Selamat datang, Admin." << endl;
    } else {
    cout << "Login GAGAL: Password salah!" << endl;
    }
    } else {
    cout << "Login GAGAL: Username tidak ditemukan!" << endl;
    }
    return 0;
    }