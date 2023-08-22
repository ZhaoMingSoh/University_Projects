#include <iostream>
#include <string>

using namespace std;

int main(){
    string one = "12";
    string two = "24";
    string sum = "";
    int k = 2;

    one += std::string(k, '0');

    cout<<one<<endl;


    return 0;
}