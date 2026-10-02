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
        if (username == "admin" && password == "admin123" ) {
            cout << "Login BERHASIL! Selamat datang, Admin." << endl;
        } else {
            cout << "Login GAGAL: Username atau Password salah!" << endl;
        }
    
    return 0;
    }