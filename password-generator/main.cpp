#include <iostream>
#include <string>
#include <algorithm>
#include <random>
#include <ctime>
#include <cctype>  // Добавлен для tolower()

using namespace std;

int main() {
    int length;
    cout << "Length (min 4): ";
    cin >> length;
    length = max(4, length);
    
    char useSpecial;
    cout << "Use special chars? (y/n): ";
    cin >> useSpecial;
    
    string lower = "abcdefghijklmnopqrstuvwxyz";
    string upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    string digits = "0123456789";
    string special = "!@#$%^&*()_+-=";
    
    // Инициализация генератора
    random_device rd;
    mt19937 rng(rd());
    
    vector<char> password = {
        lower[uniform_int_distribution<>(0, lower.size()-1)(rng)],
        upper[uniform_int_distribution<>(0, upper.size()-1)(rng)],
        digits[uniform_int_distribution<>(0, digits.size()-1)(rng)]
    };
    
    // Исправлено условие
    if (tolower(useSpecial) == 'y') {
        password.push_back(special[uniform_int_distribution<>(0, special.size()-1)(rng)]);
    }
    
    // Исправлено условие для special
    string all = lower + upper + digits + 
                (tolower(useSpecial) == 'y' ? special : "");
    
    while (password.size() < length) {
        password.push_back(all[uniform_int_distribution<>(0, all.size()-1)(rng)]);
    }
    
    shuffle(password.begin(), password.end(), rng);
    cout << "Password: " << string(password.begin(), password.end()) << endl;
    
    return 0;
}