#include <cstdlib>
#include <cctype>
#include <cstring>
#include <cstdio>
#include <cmath>
#include <algorithm>
#include <vector>
#include <string>
#include <iostream>
#include <sstream>
#include <map>
#include <set>
#include <queue>
#include <stack>
#include <fstream>
#include <numeric>
#include <iomanip>
#include <bitset>
#include <list>
#include <stdexcept>
#include <functional>
#include <utility>
#include <ctime>
using namespace std;

/*void output()
{
    int i;
    cout<<"name   arrival   end   ready   running   waiting"<<endl;
    for(i=0; i<result.size(); i++) // every result
    {

    }
    cout<<endl;
}*/

/*int main(int argc,char *argv[])
{
    int i,j,k;
    freopen(argv[1],"r",stdin);

    initial();        // initial data
    input();          // input data
    works();          // process data
    output();         // output result
    return 0;
}*/


int main(){

    ifstream in_file("./test_data_new/case0/input.txt");
    string line;
    string a;
    int b, c, d, e;
    int i = 0;

    if (in_file.is_open()){
        while( getline(in_file, line )){
           stringstream abc(line);
    
           abc >> a >> b >> c >> d >> e;                                                                                                                                                                                                                                                                                                                                                                            

           cout << a << b << c << d << e << endl;
        }
            
    }
    else{
        // Error
        cout<< "Unable to open file" <<endl;
    }

    in_file.close();

    return 0;
}

