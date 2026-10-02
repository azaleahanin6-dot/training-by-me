#include <iostream>
using namespace std;

int main(){

    double ticket_price;
    int ticket_quantity;
    double total_price;
    float discount;
    double final_price;

    ticket_price = 15000;

    cout << "input your ticket quantity: ";
    cin >> ticket_quantity ;

    total_price = (ticket_price * ticket_quantity);
    cout << total_price << endl;

    if (total_price > 45000){
        cout << "congratulation! you get 10% discount." << endl;
        discount = (total_price * 0.1);
        final_price = (total_price - discount);
        cout << "the price to pay: " << final_price << endl;
    } else {
        final_price = (total_price);
        cout << "the price to pay: " << final_price << endl;
    }

 return 0;
}