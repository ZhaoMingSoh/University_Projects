#include <iostream>
#include <string>

using namespace std;


//Convert decimal Numbers to  radix bases
string intToA(int n,int radix) 
 {
    string ans="";

    do{
        int t=n%radix;

        if(t>=0&&t<=9){
            ans+=t+'0';
        }
        else {
            ans+=t-10+'a';
        }
        n/=radix;
    }while(n!=0);   

    reverse(ans.begin(),ans.end());

    return ans;    
}

int main(){ 

    int one = 1234;
    string ans = "";

    ans+=6-10+'a';

    cout<<ans<<endl;


    return 0;

}