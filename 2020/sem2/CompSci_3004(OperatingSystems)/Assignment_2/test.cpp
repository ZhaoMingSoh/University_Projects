#include <iostream>
#include <vector>

using namespace std;

class Pages{
    public :
        int page_Num;
        int time;

        Pages(int page_Num){
            this->page_Num = page_Num;
            this->time = 0;
        }
        int get_PageNum(){
            return page_Num;
        }
        int get_Time(){
            return time;
        }
        void set_Time(int time){
            this->time = time;
        }


};

bool hit(vector <Pages> mem, int pages){
    for(int i=0; i<mem.size(); i++){
        if(mem[i].get_PageNum() == pages){
            return true;
        }
    }
    return false;
}

int main(){
    vector <int> one;
    one.push_back(8);
    one.push_back(15);
    one.push_back(13);
    one.push_back(1);
    one.push_back(7);
    one.push_back(2);

    string bits = "11010";
    bits[0] = '0';
    // char bit = ' ';
    // string temp_2;
    // // string temp_2 = "0";
    // // string temp = bits.substr(0,bits.length()-1);
    // // temp_2 += temp;

    // for(int i=0; i<bits.length(); i++){
    //     temp_2 += ((bits[i]-0));
    // }


    cout<<bits<<endl;




    // vector <Pages> mem;
    // vector <Pages> mem_Arr;
    // int time = 0;

    // for(int i=0; i<one.size(); i++){
    //     mem.push_back(Pages(one[i]));
    // }

    // time++;
    // mem[0].set_Time(time);
    // mem_Arr.push_back(mem[0]);
    // mem.erase(mem.begin());

    // while(mem_Arr.size() != 4){
    //     time++;
    //     if(hit(mem_Arr, mem[0].get_PageNum()) == false){
    //         mem[0].set_Time(time);
    //         mem_Arr.push_back(mem[0]);
    //         mem.erase(mem.begin());
    //     }else{
    //         mem.erase(mem.begin());
    //     }

    //     cout<<time<<" : ";
    //     for(int i=0; i<mem_Arr.size(); i++){
    //         cout<<mem_Arr[i].get_Time()<<" ";
    //     }
    //     cout<<endl;
    // }

    // while(mem_Arr.size() == 4 && mem.size() != 0){
    //     time++;
    //     if(hit(mem_Arr, mem[0].get_PageNum()) == false){
    //         mem[0].set_Time(time);
    //         int t = mem_Arr[0].get_Time();
    //         int index = 0;
    //         for(int i=1; i<mem_Arr.size(); i++){
    //             if(mem_Arr[i].get_Time() < t){
    //                 t = mem_Arr[i].get_Time();
    //                 index = i;
    //             }
    //         }
    //         mem_Arr.erase(mem_Arr.begin()+index);
    //         mem_Arr.insert(mem_Arr.begin()+index, mem[0]);
    //         mem.erase(mem.begin());
    //     }else{
    //         mem.erase(mem.begin());
    //     }

    //     cout<<time<<" : ";
    //     for(int i=0; i<mem_Arr.size(); i++){
    //         cout<<mem_Arr[i].get_Time()<<" ";
    //     }
    //     cout<<endl;
    //     // cout<<time<<" : ";
    //     // for(int i=0; i<mem_Arr.size(); i++){
    //     //     cout<<mem_Arr[i].get_PageNum()<<" ";
    //     // }
    //     // cout<<endl;
    // }








    return 0;
}