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

// Convert Hexadecimal to Decimal value
int Hex_To_Dec(string address, int frame_Size){
    char temp = ' ';
    int temp_Sum = 0;
    int temp_index_counter = 0;

    for(int j=address.length()-1; j>0; j--){
        temp = address[j];
        if(address[j]>= '0' && address[j]<= '9'){
            temp_Sum += ((temp-48) * pow(16,temp_index_counter));
            temp_index_counter++;
        }
        else if(address[j]>= 'a' && address[j]<= 'f'){
            temp_Sum += (((temp-97)+10) * pow(16,temp_index_counter));
            temp_index_counter++;
        }
    }

    return floor(temp_Sum/frame_Size);
}

class Pages{
    public:
        Pages(char State, string memory_Address, int page_Num){
            this->State = State;
            this->memory_Address = memory_Address;
            this->page_Num = page_Num;
        }

        // Retrieve Information
        char get_State(){
            return State;
        }

        string get_memory_Address(){
            return memory_Address;
        }

        int get_Page_Number(){
            return page_Num;
        }

        int get_Counter(){
            return counter;
        }

        string get_Referenced_Bits(){
            return referenced_Bits;
        }

        // Change Information
        void change_State(char State){
            this->State = State;
        }

        void change_Counter(int counter){
            this->counter = counter;
        }

        void set_referenced_Bits_Size(string RF){
            referenced_Bits = RF;
        }

        void set_Bit(){
            referenced_Bits[0] = '1';
        }

        void change_Bits(string referenced_Bits){
            this->referenced_Bits = referenced_Bits;
        }

    private:

        char State;
        string memory_Address;
        int page_Num;
        int counter;
        string referenced_Bits;
};

bool Hit_Or_Miss(vector <Pages> memory_Frames, int page_Num){   
    bool temp = false;
    for(int i=0; i<memory_Frames.size(); i++){
        if(memory_Frames[i].get_Page_Number() == page_Num){
            temp = true; 
        }

    }
    return temp;
}

void check_Counter(vector <Pages> &memory_Frames, Pages memory_Traces){
    int min = memory_Frames[0].get_Counter();
    for(int i=1; i<memory_Frames.size(); i++){
        if(memory_Frames[i].get_Counter() <  min){
            memory_Frames[i] = memory_Traces;
        }
    }
}

void FIFO(vector <Pages> memory_Traces, int frame_Num, int &events_Time, int &disk_Reads, int &disk_Writes, int &page_Faults){
    vector <Pages> memory_Frames;

    // Initialization
    // Load in the first page 
    memory_Frames.push_back(memory_Traces[0]);
    memory_Traces.erase(memory_Traces.begin());
    events_Time++;
    disk_Reads++;
    page_Faults++;

    // Load in the rest
    while(memory_Frames.size() != frame_Num){
        if( Hit_Or_Miss(memory_Frames, memory_Traces[0].get_Page_Number()) == false){
            memory_Frames.push_back(memory_Traces[0]);
            memory_Traces.erase(memory_Traces.begin());
            events_Time++;
            disk_Reads++;
            page_Faults++;
        }
        else{
            for(int i=0; i<memory_Frames.size(); i++){
                if(memory_Frames[i].get_Page_Number() == memory_Traces[0].get_Page_Number() && memory_Traces[0].get_State() == 'W'){
                    memory_Frames[i].change_State('W');
                }
            }
            memory_Traces.erase(memory_Traces.begin());
            events_Time++;
        }
    }

    while(memory_Frames.size() == frame_Num && memory_Traces.size() != 0){
        // If the current page number is not in the current memory frames, then proceed to do page replacement
        if(Hit_Or_Miss(memory_Frames, memory_Traces[0].get_Page_Number()) == false){

            // If memory frame is dirty meaning its state is W
            if(memory_Frames[0].get_State() == 'W'){
                disk_Writes++;
            }
            memory_Frames.erase(memory_Frames.begin());
            memory_Frames.push_back(memory_Traces[0]);
            memory_Traces.erase(memory_Traces.begin());
            events_Time++;
            disk_Reads++;
            page_Faults++;
        }else{ // If the current page number is in the current memory frames, then proceed to change the state of that memory frame state if and only if the current page state is W

            for(int i=0; i<memory_Frames.size(); i++){
                if(memory_Frames[i].get_Page_Number() == memory_Traces[0].get_Page_Number() && memory_Traces[0].get_State() == 'W'){
                    memory_Frames[i].change_State('W');
                }
            }
            memory_Traces.erase(memory_Traces.begin());
            events_Time++;
        }
    }
}

void LRU(vector <Pages> memory_Traces, int frame_Num, int &events_Time, int &disk_Reads, int &disk_Writes, int &page_Faults){
    vector <Pages> memory_Frames;

    events_Time++;
    memory_Traces[0].change_Counter(events_Time);
    memory_Frames.push_back(memory_Traces[0]);
    memory_Traces.erase(memory_Traces.begin());
    disk_Reads++;
    page_Faults++;

    while(memory_Frames.size() != frame_Num){
        events_Time++;
        if(Hit_Or_Miss(memory_Frames, memory_Traces[0].get_Page_Number()) == false){
            memory_Traces[0].change_Counter(events_Time);
            memory_Frames.push_back(memory_Traces[0]);
            memory_Traces.erase(memory_Traces.begin());
            disk_Reads++;
            page_Faults++;
        }else{
            for(int i=0; i<memory_Frames.size(); i++){
                if(memory_Frames[i].get_Page_Number() == memory_Traces[0].get_Page_Number()){
                    memory_Frames[i].change_Counter(events_Time);
                }
                if(memory_Frames[i].get_Page_Number() == memory_Traces[0].get_Page_Number() && memory_Traces[0].get_State() == 'W'){
                    memory_Frames[i].change_State('W');
                }
            }
            memory_Traces.erase(memory_Traces.begin());
        }
    }

    while(memory_Frames.size() == frame_Num && memory_Traces.size() != 0){
        if(Hit_Or_Miss(memory_Frames, memory_Traces[0].get_Page_Number()) == false){
            events_Time++;
            memory_Traces[0].change_Counter(events_Time);
            int time_min = memory_Frames[0].get_Counter();
            int min_index = 0;
            for(int i=1; i<memory_Frames.size(); i++){
                if(memory_Frames[i].get_Counter() < time_min){
                    time_min = memory_Frames[i].get_Counter();
                    min_index = i;
                }
            }
            if(memory_Frames[min_index].get_State() == 'W'){
                disk_Writes++;
            }
            memory_Frames.erase(memory_Frames.begin()+min_index);
            memory_Frames.insert(memory_Frames.begin()+min_index, memory_Traces[0]);
            memory_Traces.erase(memory_Traces.begin());
            disk_Reads++;
            page_Faults++;
        }else{
            events_Time++;
            for(int i=0; i<memory_Frames.size(); i++){
                if(memory_Frames[i].get_Page_Number() == memory_Traces[0].get_Page_Number()){
                    memory_Frames[i].change_Counter(events_Time);
                }
                if(memory_Frames[i].get_Page_Number() == memory_Traces[0].get_Page_Number() && memory_Traces[0].get_State() == 'W'){
                    memory_Frames[i].change_State('W');
                }
            }
            memory_Traces.erase(memory_Traces.begin());
        }
    }

    
}

void set_size_Of_referenced_Bits(int size_Of_RF, vector <Pages> &memory_Traces){
    string temp = "";
    for(int i=0; i<size_Of_RF; i++){
        temp += '0';
    }
    
    for(int i=0; i<memory_Traces.size(); i++){
        memory_Traces[i].set_referenced_Bits_Size(temp);
    }
}

void reset_Bit(vector <Pages> &memory_Frames, int num_Bits){
    string temp = "";
    string temp_2 = "";
    string temp_3 = "0";
    if(num_Bits == 1){
        for(int i=0; i<memory_Frames.size(); i++){
            memory_Frames[i].change_Bits("0");
        }
    }else{
        for(int i=0; i<memory_Frames.size(); i++){
            temp = memory_Frames[i].get_Referenced_Bits();
            temp_2 = temp.substr(0,temp.length()-1);
            temp_3 += temp_2;
            memory_Frames[i].change_Bits(temp_3);
            temp_3 = "0";
        }
    }
}

int sum_Bits(string memory_Frames, int num_Bits){
    int sum = 0;
    int index = 0;
    for(int i=num_Bits-1; i>=0; i--){
        sum += (memory_Frames[i]-0)*pow(2,index);
        index++;
    }

    return sum;
}

void sort_Frames(vector <Pages> &memory_Frames){
    int time = 0;
    int hole = 0;
    for(int i=1; i<memory_Frames.size(); i++){
        time = memory_Frames[i].get_Counter();
        Pages temp = memory_Frames[i];
        hole = i-1;
        while(hole>=0 && memory_Frames[hole].get_Counter() > time){
            memory_Frames[hole+1] = memory_Frames[hole];
            hole--;
        }
        memory_Frames[hole+1] = temp;
    }
}

int check_Bits(vector <Pages> memory_Frames, int num_Bits){
    bool temp = false; 
    int index = 0;
    int min_Sum = sum_Bits(memory_Frames[0].get_Referenced_Bits(), num_Bits);

    if(num_Bits == 1){
        while(temp == false){
            for(int i=0; i<memory_Frames.size(); i++){
                if(memory_Frames[i].get_Referenced_Bits() == "0"){
                    index = i;
                    temp = true;
                    break;
                }else{
                    memory_Frames[index].change_Bits("0");
                }
            }
        }
    }else{
        for(int i=0; i<memory_Frames.size(); i++){
            if(sum_Bits(memory_Frames[i].get_Referenced_Bits(), num_Bits) < min_Sum){
                min_Sum = sum_Bits(memory_Frames[i].get_Referenced_Bits(), num_Bits);
                index = i;
            }
        }
    
    }

    return index;
}
        

void ARB(vector <Pages> memory_Traces, int frame_Num, int &events_Time, int &disk_Reads, int &disk_Writes, int &page_Faults, int register_Shifting, int num_Bits){
    vector <Pages> memory_Frames;

    // Initialization 
    events_Time++;
    memory_Traces[0].change_Counter(events_Time);
    memory_Frames.push_back(memory_Traces[0]);
    memory_Frames[0].set_Bit();
    memory_Traces.erase(memory_Traces.begin());
    disk_Reads++;
    page_Faults++;

    while(memory_Frames.size() != frame_Num){
        events_Time++;
        if(Hit_Or_Miss(memory_Frames, memory_Traces[0].get_Page_Number()) == false){
            memory_Traces[0].change_Counter(events_Time);
            memory_Traces[0].set_Bit();
            memory_Frames.push_back(memory_Traces[0]);
            memory_Traces.erase(memory_Traces.begin());
            disk_Reads++;
            page_Faults++;
        }else{
            for(int i=0; i<memory_Frames.size(); i++){
                if(memory_Frames[i].get_Page_Number() == memory_Traces[0].get_Page_Number()){
                    memory_Frames[i].set_Bit();
                }
                if(memory_Frames[i].get_Page_Number() == memory_Traces[0].get_Page_Number() && memory_Traces[0].get_State() == 'W'){
                    memory_Frames[i].change_State('W');
                }
            }
            memory_Traces.erase(memory_Traces.begin());
        }
        if(events_Time % register_Shifting == 0){
            reset_Bit(memory_Frames, num_Bits);
        }
    }

    // Page Replacement
    while(memory_Frames.size() == frame_Num && memory_Traces.size() != 0){
        events_Time++;
        if(Hit_Or_Miss(memory_Frames, memory_Traces[0].get_Page_Number()) == false){
            sort_Frames(memory_Frames);
            int index = check_Bits(memory_Frames, num_Bits);

            memory_Traces[0].change_Counter(events_Time);
            memory_Traces[0].set_Bit();
            if(memory_Frames[index].get_State() == 'W'){
                disk_Writes++;
            }
            memory_Frames[index] = memory_Traces[0];
            memory_Traces.erase(memory_Traces.begin());
            disk_Reads++;
            page_Faults++;
        }else{
            sort_Frames(memory_Frames);
            for(int i=0; i<memory_Frames.size(); i++){
                if(memory_Frames[i].get_Page_Number() == memory_Traces[0].get_Page_Number()){
                    memory_Frames[i].set_Bit();
                }
                if(memory_Frames[i].get_Page_Number() == memory_Traces[0].get_Page_Number() && memory_Traces[0].get_State() == 'W'){
                    memory_Frames[i].change_State('W');
                }
            }
            memory_Traces.erase(memory_Traces.begin());
        }
        sort_Frames(memory_Frames);
        if(events_Time % register_Shifting == 0){
            reset_Bit(memory_Frames, num_Bits);
        }
        // cout<<events_Time<<" : ";
        // for(int i=0; i<memory_Frames.size(); i++){
        //     cout<<memory_Frames[i].get_Page_Number()<<" ";
        // }
        // cout<<endl;
        // cout<<"Bits : ";
        // for(int i=0; i<memory_Frames.size(); i++){
        //     cout<<memory_Frames[i].get_Referenced_Bits()<<" ";
        // }
        // cout<<endl;

        // cout<<"Counter : ";
        // for(int i=0; i<memory_Frames.size(); i++){
        //     cout<<memory_Frames[i].get_Counter()<<" ";
        // }
        // cout<<endl;
    }
    
}

void WSARB_1(){

}

int main(int num_Inputs, char* string_Inputs[]){
    // Reading the input file, the page size, the number of page frames and the type of Page Replacement algorithm to run 
    string input_File;
    int frame_Size;
    int frame_Number;
    string PG_Algorithm;

    if(num_Inputs > 1){
        input_File = string_Inputs[1];
        frame_Size = stoi(string_Inputs[2]);
        frame_Number = stoi(string_Inputs[3]);
        PG_Algorithm = string_Inputs[4];
    }

    string memory_traces;
    ifstream myfile (input_File);
    vector <string> mem_Arr;
    vector <Pages> memory_Traces;
    char state;
    string memory_Addr;
    int page_Num;
    
    // Reading in the input.txt 
    if(myfile.is_open()){
        while(getline(myfile,memory_traces)){
            mem_Arr.push_back(memory_traces);
        }
    }
    else{
        cout<<"Unable to Open File !!"<<endl;
    }

    myfile.close();

    // Creating page from memory trace  
    for(int i=1; i<mem_Arr.size(); i++){
        stringstream ss(mem_Arr[i]);
        ss >> state >> memory_Addr;
        memory_Traces.push_back(Pages(state, memory_Addr, Hex_To_Dec(memory_Addr, frame_Size)));
    }

    int events_Time = 0;
    int disk_Reads = 0;
    int disk_Writes = 0;
    int page_Faults = 0;

    if(PG_Algorithm == "FIFO"){
        FIFO(memory_Traces, frame_Number, events_Time, disk_Reads, disk_Writes, page_Faults);
    }
    else if(PG_Algorithm == "LRU"){
        LRU(memory_Traces, frame_Number, events_Time, disk_Reads, disk_Writes, page_Faults);
    }
    else if(PG_Algorithm == "ARB"){
        int num_Bits = stoi(string_Inputs[5]);
        int register_Shifting = stoi(string_Inputs[6]);
        set_size_Of_referenced_Bits(num_Bits, memory_Traces);
        ARB(memory_Traces, frame_Number, events_Time, disk_Reads, disk_Writes, page_Faults, register_Shifting, num_Bits);
    }else if(PG_Algorithm == "WSARB-1"){
        int num_Bits = stoi(string_Inputs[5]);
        int register_Shifting = stoi(string_Inputs[6]);
        int working_Set_Size = stoi(string_Inputs[7]);
        
    }

    cout<<"events in trace: "<<events_Time<<endl;
    cout<<"total disk reads: "<<disk_Reads<<endl;
    cout<<"total disk writes: "<<disk_Writes<<endl;
    cout<<"page faults: "<<page_Faults<<endl;
    // int c = 1;
    // for(int i=0; i<memory_Traces.size(); i++){
    //     cout<<c+i<<" : "<<memory_Traces[i].get_State()<<" "<<memory_Traces[i].get_memory_Address()<<" : "<<memory_Traces[i].get_Page_Number()<<endl;
    // }

    // for(int i=0; i<mem_Arr.size(); i++){
    //     cout<<mem_Arr[i+1]<<endl;
    // }

    // cout<<mem_Arr[frame_Number+1]<<endl;


    return 0;
}