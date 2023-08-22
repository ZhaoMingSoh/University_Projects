#include<iostream>
#include<string>
#include <algorithm>
#include <sstream>
using namespace std;
//remove the '0' before the string
void removePreZero(string &str) {
    //if the length of the string is 1, return
    if (str.length() == 1)return;
    unsigned int k = 0;
    //calculate the num of '0' before the string
    for (unsigned int i = 0; i < str.length(); i++) {
        if (str.at(i) == '0') {
            k++;
        } else {
            break;
        }
    }
    //removte the first k char of string
    if (k == str.length())str = "0";
    else {
        str = str.substr(k);
    }
}
//School mathod of inteager addition
string schoolmethod(string s1,string s2,int base){
	string sum;
    //remove the '0' before the s1,s2
	removePreZero(s1);
    removePreZero(s2);
    // let s1 is the longer string
	if (s1.size() < s2.size())
{
string temp = s1;
s1 = s2;
s2 = temp;
}
//fill '0' before the s2 ,let the length of s1 equal the length of s2 
int len = s1.size() - s2.size();
string s3(len, '0');
s2 = s3 + s2;
int a = 0;
//do addition character by character ,if the result>base,then a=1,result=reuslt -base
for (int i = s1.size() - 1; i >= 0; i--)
{
int b = (s1[i] - '0') + (s2[i] - '0') + a;
if (b > (base-1))
{
sum.push_back((b-base)+'0');
a = 1;
}
else{
sum.push_back(b+'0');
a=0;}
}
sum.push_back(a+'0');
//reverse the result
reverse(sum.begin(),sum.end());
//remove the '0' before the result
removePreZero(sum);
return sum;
}
//School mathod of inteager substract 
string subtract(string s1,string s2,int base){
	string result;
     //remove the '0' before the s1,s2
	removePreZero(s1);
    removePreZero(s2);
    // let s1 is the longer string
	if (s1.size() < s2.size())
{
string temp = s1;
s1 = s2;
s2 = temp;
}
//fill '0' before the s2 ,let the length of s1 equal the length of s2 
int len = s1.size() - s2.size();
string s3(len, '0');
s2 = s3 + s2;
int a = 0;
//do substract character by character
for (int i = s1.size() - 1; i >= 0; i--)
{
	if((s1[i]-a)>=s2[i]){
		int b = (s1[i] - '0') - (s2[i] - '0') -a;
		result.push_back(b+'0');
		a=0;
	}
	
	else{
		int b = (s1[i] - '0')+base - (s2[i] - '0') -a;
		result.push_back(b+'0');
		a=1;
	}
	
}
//reverse the result
reverse(result.begin(),result.end());
//remove the '0' before the result               
removePreZero(result);
return result;
}
//chage the int to string;
string inttoStr(int intValue) {
    string result;
    stringstream stream;
    stream << intValue;
    stream >> result;
    return result;
}
//add  zero_num  '0' before the string 
void addPreZero(string &str, int zero_num) {
    for (int i = 0; i < zero_num; i++)str.insert(0, "0");
}
//把str乘以base的zero_num次方（base就是进制为2到10整数）
string addLastZero(string str, int zero_num) {
    string s = str;
    for (int i = 0; i < zero_num; i++)s += "0";
    return s;
}
//Convert decimal Numbers to  radix bases
string intToA(int n,int radix) 
 {
    string ans="";
    do{
        int t=n%radix;
        if(t>=0&&t<=9)    ans+=t+'0';
        else ans+=t-10+'a';
        n/=radix;
    }while(n!=0);    
    reverse(ans.begin(),ans.end());
    return ans;    
}
//product in KaraTsuba algorithm
string KaraTsuba(string &x, string &y,int base) {

    //Change the length of a character to a multiple of 2,If the number of digits is insufficient, fill in 0
    unsigned int init_len = 4;
    if (x.length() > 2 || y.length() > 2) { 
        if (x.length() >= y.length()) {
            while (init_len < x.length())init_len *= 2; 
            if (x.length() != init_len) {
                addPreZero(x, init_len - x.length());
            }
            addPreZero(y, init_len - y.length());
        } else {
            while (init_len < y.length())init_len *= 2;
            addPreZero(x, init_len - x.length());
            if (y.length() != init_len) {
                addPreZero(y, init_len - y.length());
            }
        }
    }
    //if the string length is 1,the fill a '0' before the string
    if (x.length() == 1) {
        addPreZero(x, 1);
    }
    if (y.length() == 1) {
        addPreZero(y, 1);
    }

    int n = x.length();

    string result;

    string a1, a0, b1, b0;
    if (n > 1) {
        //Split by half of the string
        a1 = x.substr(0, n / 2);
        a0 = x.substr(n / 2, n);
        b1 = y.substr(0, n / 2);
        b0 = y.substr(n / 2, n);
    }

    if (n == 2) {
        //when the length of string is 2,calculate the result 
        int x1 = stoi(a1);
        int x2 = stoi(a0);
        int y1 = stoi(b1);
        int y2 = stoi(b0);
        int z = (x1 * base + x2) * (y1 * base + y2);
        //if base is not decimal,then Convert decimal Numbers to  radix bases
        if(base!=10)
       result=intToA(z,base);
    	else
    		result=inttoStr(z);

    } else {
        //recursive the function until n is 2;
        //c2=a1*b1
        string c2 = KaraTsuba(a1, b1,base);
        //c0=a0*b0
        string c0 = KaraTsuba(a0, b0,base);
        //temp_c1_1=a0+a1;
        string temp_c1_1 = schoolmethod(a0, a1,base);
        //temp_c1_2=b1+b0;
        string temp_c1_2 = schoolmethod(b1, b0,base);
        //temp_c1_3=c2+c0;
        string temp_c1_3 = schoolmethod(c2, c0,base);
        //temp_c1=(a0+a1)*(b0+b1)
        string temp_c1 = KaraTsuba(temp_c1_1, temp_c1_2,base);
        //c1=(a0+a1)*(b0+b1)-(c2+c0)=a0*b1+a1*b0
        string c1 = subtract(temp_c1, temp_c1_3,base);
        string s1 = addLastZero(c1, n / 2);
        string s2 = addLastZero(c2, n);
        //result=c1+c2+c0=（a0*b0+a0*b1）*base的2/n次方+a1*b1+a0*b0*base的n次方------详见KaraTsuba算法公式
        result = schoolmethod(schoolmethod(s1, s2,base), c0,base);
    }


    return result;
}
//overwtrite the KaraTsuba function for different type of parameter
string KaraTsuba(string x, int y,int base) {
    string temp = inttoStr(y);
    return KaraTsuba(x, temp,base);
}
  
string KaraTsuba(int x, string y,int base) {
    string temp = inttoStr(x);
    return KaraTsuba(temp, y, base);
}

string KaraTsuba(int x, int y,int base ) {
    string temp1 = inttoStr(x);
    string temp2 = inttoStr(y);
    return KaraTsuba(temp1, temp2,base);
}
int main()
{
string s1, s2, sum,mul;
int base;
cin >> s1>>s2>>base;
sum=schoolmethod(s1,s2,base);
mul=KaraTsuba(s1,s2,base);

cout<<sum<<" "<<mul<<endl;
return 0;
}
