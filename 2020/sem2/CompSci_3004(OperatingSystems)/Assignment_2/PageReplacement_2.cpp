//a1751699 Zhao Ming Soh
//a1753701 Jinghong Xiong
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
#include <stdlib.h> 
using namespace std;

int topage(char hax[ ],int num){
    int length = strlen(hax);
    int base = 1;
    int result = 0;
    for(int i=length-1;i>=0;i--){
        if(hax[i]>='0' && hax[i]<='9'){
            result+=(hax[i]-48)*base;
        }else if(hax[i]>='a' && hax[i]<='f'){
            result+=(hax[i]-87)*base;
        }
        base *= 16;
    }
    return result =result/num;
}

class Pages{
    public:
    Pages(char type,char address[ ],int num){
        this->type = type;
        this->address = string(address);
        page_num = topage(address,num);
        remain_time=0;
    }
    int get_page_num(){
        return page_num;
    }
    string get_address(){
        return address;
    }
    char get_type(){
        return type;
    }
    void change_type(char type){
        this->type=type;
    }
    int get_remain_time(){
        return remain_time;
    }
    void change_remain_time(int remain_time){
        this->remain_time=remain_time;
    }
    void set_bits(int num){
        for(int i=0;i<num;i++){
            bits.push_back(0);
        }
    }
    void initiall_bits(){
        bits.insert(bits.begin(),1);
        bits.pop_back();
    }
    void shift_bits(){
        bits.insert(bits.begin(),0);
        bits.pop_back();
    }
    int get_bits(){
        int result=0;
        int base=1;
        for(int i=bits.size()-1;i>=0;i--){
            result+=bits[i]*base;
            base *= 10;
        }
        return result;
    }
    void hit_bit(){
        if(bits[0]==0){
            bits.erase(bits.begin());
            bits.insert(bits.begin(),1);
        }
    }
    private:
    char type;
    string address;
    int page_num;
    int remain_time;
    vector<int> bits;
};

bool check_hit(vector<Pages> &frame,Pages current){
    for(int i=0;i<frame.size();i++){
        if(frame[i].get_page_num()==current.get_page_num()){
            if(frame[i].get_bits()!=0){
                frame[i].hit_bit();
            }
            if(current.get_type()=='W'){
                frame[i].change_type('W');
            }
            frame[i].change_remain_time(-1);
            return true;
        }
    }
    return false;
}

void FIFO(vector<Pages> input_value,int &event,int &reads,int &writes,int &pagefalts,int frame_length){
    event=0;reads=0;writes=0;pagefalts=0;
    vector<Pages> frame;
    while (input_value.size()!=0){
        event++;
        if(frame.size()<frame_length){
            if(check_hit(frame,input_value[0])){
                //cout<<"hit in :"<<event<<endl;
                input_value.erase(input_value.begin());
            }else{
                
                reads++;
                pagefalts++;
                
                
                frame.push_back(input_value[0]);
                input_value.erase(input_value.begin());
            }
            
        }else{
            if(check_hit(frame,input_value[0])){
                //cout<<"hit in :"<<event<<endl;
                input_value.erase(input_value.begin());
            }else{
                if(frame[0].get_type()=='W'){
                    writes++;
                }
                reads++;
                pagefalts++;
                frame.erase(frame.begin());
                frame.push_back(input_value[0]);
                input_value.erase(input_value.begin());
            }
        }
    }
}
void sort_remain_time(vector<Pages> &frame){
    int i,key,j;
    for(int i=1;i<frame.size();i++){
        key=frame[i].get_remain_time();
        j=i-1;
        while(j>=0 && frame[j].get_remain_time()<key){
            swap(frame[j+1],frame[j]);
            j=j-1;            
        }
    }
}
void increase_remain_time(vector<Pages> &frame){
    for(int i=0;i<frame.size();i++){
        frame[i].change_remain_time(frame[i].get_remain_time()+1);
    }
}

void LRU(vector<Pages> input_value,int &event,int &reads,int &writes,int &pagefalts,int frame_length){
    event=0;reads=0;writes=0;pagefalts=0;
    vector<Pages> frame;
    while (input_value.size()!=0){
        event++;
        sort_remain_time(frame);
        if(frame.size()<frame_length){
            if(check_hit(frame,input_value[0])){
                //cout<<"hit in :"<<event<<endl;
                input_value.erase(input_value.begin());
                increase_remain_time(frame);
                sort_remain_time(frame);
            }else{
                reads++;
                pagefalts++;
                increase_remain_time(frame);
                
                frame.push_back(input_value[0]);
                input_value.erase(input_value.begin());
                sort_remain_time(frame);
            }
            
        }else{
            if(check_hit(frame,input_value[0])){
                //cout<<"hit in :"<<event<<endl;
                input_value.erase(input_value.begin());
                increase_remain_time(frame);
                sort_remain_time(frame);
            }else{
                
                reads++;
                pagefalts++;
                sort_remain_time(frame);
                increase_remain_time(frame);
                if(frame[0].get_type()=='W'){
                    writes++;
                    //cout<<"write in "<<event<<endl;
                }
                frame.erase(frame.begin());
                frame.push_back(input_value[0]);
                input_value.erase(input_value.begin());
            }
        }
    }   
}
void sort_bit(vector<Pages> &frame){
    int i,key,j;
    for(int i=1;i<frame.size();i++){
        key=frame[i].get_bits();
        j=i-1;
        while(j>=0 && frame[j].get_remain_time()>key){
            swap(frame[j+1],frame[j]);
            j=j-1;            
        }
    }
}
int remove_bit(vector<Pages> &frame,int bits){
    int result = -1;
    int initial_bit = 0;
    int base=1;
    for(int i=0;i<bits;i++){
        initial_bit+=1*base;
        base *= 10;
    }
    //cout<<"initial_bit: "<<initial_bit<<endl;
    for(int i=0;i<frame.size();i++){
        if(frame[i].get_bits()<initial_bit){
            initial_bit=frame[i].get_bits();
            result=i;
        }
    }
    return result ;
}

void ARB(vector<Pages> input_value,int &event,int &reads,int &writes,int &pagefalts,int frame_length,int bits,int time_interval){
    for(int i=0;i<input_value.size();i++){
        input_value[i].set_bits(bits);
    }
    event=0;reads=0;writes=0;pagefalts=0;
    vector<Pages> frame;
    while(input_value.size()!=0){
        event++;
        if(((event-1)%time_interval==0) && (event!=0)){
            for(int i=0;i<frame.size();i++){
                frame[i].shift_bits();
            }
        }
        if(frame.size()<frame_length){
            if(check_hit(frame,input_value[0])){
                input_value.erase(input_value.begin());
            }else{
                reads++;
                pagefalts++;
                
                if(input_value[0].get_bits()==0){
                    input_value[0].initiall_bits();
                }
                frame.push_back(input_value[0]);
                input_value.erase(input_value.begin());
            }
        }else{
            if(check_hit(frame,input_value[0])){
                input_value.erase(input_value.begin());
            }else{
                reads++;
                pagefalts++;
                
                if(input_value[0].get_bits()==0){
                    input_value[0].initiall_bits();
                }
                int index = remove_bit(frame,bits);
                if(event==25){
                    for(int i=0;i<frame.size();i++){
                        //cout<<frame[i].get_page_num()<<"    "<<frame[i].get_bits()<<"    "<<frame[i].get_remain_time()<<endl;
                    }
                    //cout<<input_value[0].get_bits()<<endl;
                    //cout<<"index:  "<<index<<endl;
                }
                if(index != -1){
                    if(frame[0+index].get_type()=='W'){
                        writes++;
                        //cout<<"remove "<<frame[0+index].get_page_num()<<" at "<<event<<" W "<<endl;
                    }else{
                        //cout<<"remove "<<frame[0+index].get_page_num()<<" at "<<event<<endl;
                    }
                    frame.erase(frame.begin()+index);
                }else{
                    if(frame[0].get_type()=='W'){
                        writes++;
                        //cout<<"remove "<<frame[0].get_page_num()<<" at "<<event<<" W "<<endl;
                    }else{
                        //cout<<"remove "<<frame[0].get_page_num()<<" at "<<event<<endl;
                    }
                    frame.erase(frame.begin());
                }

                frame.push_back(input_value[0]);
                input_value.erase(input_value.begin());
            }
        }
        
    }
}

int find_frequency(vector<Pages> Working_set,Pages current){
    int key=current.get_page_num();
    int count=0;
    for(int i=0;i<Working_set.size();i++){
        if(Working_set[i].get_page_num()==key){
            count++;
        }
    }
    return count;
}

vector<Pages> check_working_set(vector<Pages> Working_set,vector<Pages> frame){
    vector<Pages> result;
    int frequency=Working_set.size();
    for(int i=0;i<frame.size();i++){
        if(find_frequency(Working_set,frame[i])<frequency){
            result.clear();
            frequency=find_frequency(Working_set,frame[i]);
            result.push_back(frame[i]);
        }else if(find_frequency(Working_set,frame[i])==frequency){
            result.push_back(frame[i]);
        }
    }
    return result;
}
Pages find_remove(vector<Pages> frame,int bits){
    int initial_bit = 0;
    int base=1;
    int result = -1;
    for(int i=0;i<bits;i++){
        initial_bit+=1*base;
        base *= 10;
    }
    //cout<<"initial_bit: "<<initial_bit<<endl;
    for(int i=0;i<frame.size();i++){
        if(frame[i].get_bits()<initial_bit){
            initial_bit=frame[i].get_bits();
            result=i;
        }
    }
    if(result !=-1){
        return frame[result];
    }else{
        return frame[0];
    }
    
}
int find_index(vector<Pages> frame,Pages current){
    for(int i=0;i<frame.size();i++){
        if(frame[i].get_page_num()==current.get_page_num()){
            return i;
        }
    }
    return -1;
}

void WSARB(vector<Pages> input_value,int &event,int &reads,int &writes,int &pagefalts,int frame_length,int bits,int time_interval,int working_set){
    for(int i=0;i<input_value.size();i++){
        input_value[i].set_bits(bits);
    }
    event=0;reads=0;writes=0;pagefalts=0;
    vector<Pages> frame;
    vector<Pages> Working_set;
    while(input_value.size()!=0){
        event++;
        Working_set.push_back(input_value[0]);
        if(Working_set.size()>working_set){
            Working_set.erase(Working_set.begin());
        }
        //ARB
        if(((event-1)%time_interval==0) && (event!=0)){
            for(int i=0;i<frame.size();i++){
                frame[i].shift_bits();
            }
        }
        if(frame.size()<frame_length){
            if(check_hit(frame,input_value[0])){
                input_value.erase(input_value.begin());
            }else{
                reads++;
                pagefalts++;
                
                if(input_value[0].get_bits()==0){
                    input_value[0].initiall_bits();
                }
                frame.push_back(input_value[0]);
                input_value.erase(input_value.begin());
            }
        }else{
            if(check_hit(frame,input_value[0])){
                input_value.erase(input_value.begin());
            }else{
                reads++;
                pagefalts++;
                
                if(input_value[0].get_bits()==0){
                    input_value[0].initiall_bits();
                }
                vector<Pages> F=check_working_set(Working_set,frame);
                Pages remove_page=find_remove(F,bits);
                int index = find_index(frame,remove_page);
                
                if(index != -1){
                    if(frame[0+index].get_type()=='W'){
                        writes++;
                        //cout<<"remove "<<frame[0+index].get_page_num()<<" at "<<event<<" W "<<endl;
                    }else{
                        //cout<<"remove "<<frame[0+index].get_page_num()<<" at "<<event<<endl;
                    }
                    frame.erase(frame.begin()+index);
                }else{
                    if(frame[0].get_type()=='W'){
                        writes++;
                        //cout<<"remove "<<frame[0].get_page_num()<<" at "<<event<<" W "<<endl;
                    }else{
                        //cout<<"remove "<<frame[0].get_page_num()<<" at "<<event<<endl;
                    }
                    frame.erase(frame.begin());
                }

                frame.push_back(input_value[0]);
                input_value.erase(input_value.begin());
            }
        }

    }
}


int main(int argc,char** argv){
    ifstream myfile(argv[1]);
    int max_length=stoi(argv[2]);
    int frame_length=stoi(argv[3]);
    string algorithm=argv[4];
    string Input_line;
    vector<Pages> input_value;
    char first;
    string num;
    if (myfile.is_open()){
        while ( getline (myfile,Input_line) ){
            if(Input_line[0]!='#'){
                stringstream input(Input_line);
                //input.push_back(Input_line);
                input >>first >>num;
                char *c =new char[num.length()+1];
                strcpy(c,num.c_str());
                //cout<< c <<endl;
                input_value.push_back(Pages(first,c,max_length));
                delete [] c;
            }
        }
        myfile.close();
    } 
    // for(int i=0;i<input_value.size();i++){
    //     cout<<input_value[i].get_address()<<"   "<<input_value[i].get_page_num()<<endl;
    // }
    int event,reads,writes,pagefaults;
    if(algorithm=="FIFO"){
        FIFO(input_value,event,reads,writes,pagefaults,frame_length);
        
    }else if(algorithm=="LRU"){
        LRU(input_value,event,reads,writes,pagefaults,frame_length);
    }else if(algorithm=="ARB"){
        int bits = stoi(argv[5]);
        int time_interval = stoi(argv[6]);
        ARB(input_value,event,reads,writes,pagefaults,frame_length,bits,time_interval);
    }else{
        int bits = stoi(argv[5]);
        int time_interval = stoi(argv[6]);
        int working_set=stoi(argv[7]);
        WSARB(input_value,event,reads,writes,pagefaults,frame_length,bits,time_interval,working_set);
    }
    cout<<"events in trace:"<<event<<endl;
    cout<<"total disk reads:"<<reads<<endl;
    cout<<"total disk writes:"<<writes<<endl;
    cout<<"page faults:"<<pagefaults<<endl;
}