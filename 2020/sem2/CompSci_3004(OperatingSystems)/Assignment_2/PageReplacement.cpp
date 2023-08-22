#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cmath>
#include <math.h> 
#include <deque>

using namespace std;

// Convert Hexadecimal to Decimal value
void Hex_To_Dec(vector <string> &hex, vector <int> &dec){
    char temp = ' ';
    string hex_temp = " ";
    int temp_index_counter = 0;
    int temp_Sum = 0;
    int hex_length = 0;

    for(int i=1; i<hex.size(); i++){
        hex_length = hex[i].length();   
        hex_temp = hex[i];
        temp_index_counter = 0;
        temp_Sum = 0;
        for(int j=hex_length-1; j>0; j--){
            temp = hex_temp[j];
            if(hex_temp[j]>= '0' && hex_temp[j]<= '9'){
                temp_Sum += ((temp-48) * pow(16,temp_index_counter));
                temp_index_counter++;
            }
            else if(hex_temp[j]>= 'a' && hex_temp[j]<= 'f'){
                temp_Sum += (((temp-97)+10) * pow(16,temp_index_counter));
                temp_index_counter++;
            }
        }
        dec.push_back(temp_Sum);
    }

}

// Calculate page number 
void Dec_To_Page(vector <string> &hex, vector <int> &dec, int frame_Size, vector <int> &page_Num){
    for(int i=0; i<dec.size(); i++){
        page_Num.push_back(floor(dec[i]/frame_Size));
    }
}

bool same_Or_not(deque <int> memory_Frame, int page_Num){
    bool temp = false;

    // cout<<"Page_Num : "<<page_Num<<"                     ";
    for(int i=0; i<memory_Frame.size(); i++){
        // cout<<memory_Frame[i]<<" ";
        if(memory_Frame[i] == page_Num){
            temp = true;
        }
    } 

    return temp;
}

// FIFO Page Replacement Algorithm 
void FIFO(vector <string> &hex, vector <int> page_Num, vector <char> page_State, int frame_Num, int &event_Time, int &disk_Reads, int &disk_Writes, int &page_Faults){
    deque <int> memory_Frame;
    deque <char> memory_State;

    // deque <int> disk_page;
    // deque <char> disk_State;

    memory_Frame.push_front(page_Num[0]);
    memory_State.push_front(page_State[0]);
    page_Num.erase(page_Num.begin()+0);
    page_State.erase(page_State.begin()+0);

    event_Time++;
    disk_Reads++;
    page_Faults++;

    while(memory_Frame.size() != frame_Num){
        if( same_Or_not(memory_Frame, page_Num[0]) == false){
            memory_Frame.push_back(page_Num[0]);
            memory_State.push_back(page_State[0]);
            page_Num.erase(page_Num.begin());
            page_State.erase(page_State.begin());
            event_Time++;
            disk_Reads++;
            page_Faults++;
        }
        else{
            for(int i=0; i<memory_Frame.size(); i++){
                if(memory_Frame[i] == page_Num[0] && page_State[0] == 'W'){
                    memory_State[i] = 'W';
                }
            }
            page_Num.erase(page_Num.begin());
            page_State.erase(page_State.begin());
            event_Time++;
        }

    }

    while(memory_Frame.size() == frame_Num && page_Num.size() != 0 && page_State.size() != 0){
        if(same_Or_not(memory_Frame, page_Num[0]) == false){
            event_Time++;

            if(memory_State.front() == 'W'){
                disk_Writes++;
            }

            memory_Frame.pop_front();
            memory_State.pop_front();

            memory_Frame.push_back(page_Num[0]);
            memory_State.push_back(page_State[0]);
            page_Num.erase(page_Num.begin());
            page_State.erase(page_State.begin());
            disk_Reads++;
            page_Faults++;

        }else{
            event_Time++;
            for(int i=0; i<memory_Frame.size(); i++){
                if(memory_Frame[i] == page_Num[0] && page_State[0] == 'W'){
                    memory_State[i] = 'W';
                }
            }
            page_Num.erase(page_Num.begin());
            page_State.erase(page_State.begin());

        }
    }
}

/** What is argc and argv ? 
 *  1) argc is the number of things that you enter into the command line as you run a program 
 *  2) argv holds the string value that we enter into the command line as you run a program
 * */

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
    vector <int> decimal_Val;
    vector <int> page_Num;
    vector <char> page_State;
    
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

    Hex_To_Dec(mem_Arr, decimal_Val);
    Dec_To_Page(mem_Arr, decimal_Val, frame_Size, page_Num);
    string temp = " ";
    string temp2 = " ";
    string temp3 = " ";

    for(int i=0; i<page_Num.size(); i++){
        temp = mem_Arr[i+1].at(0);
        // temp2 = to_string(page_Num[i]);
        // temp3 = temp +" "+ temp2;
        page_State.push_back(mem_Arr[i+1].at(0));
    }

    int events_Time = 0;
    int disk_Reads = 0;
    int disk_Writes = 0;
    int page_Faults = 0;

    if(PG_Algorithm == "FIFO"){
        FIFO(mem_Arr, page_Num, page_State, frame_Number, events_Time, disk_Reads, disk_Writes, page_Faults);
    }

    cout<<"events in trace: "<<events_Time<<endl;
    cout<<"total disk reads: "<<disk_Reads<<endl;
    cout<<"total disk writes: "<<disk_Writes<<endl;
    cout<<"page faults: "<<page_Faults<<endl;

    // for(int i=0; i<page_State.size(); i++){
    //     cout<<mem_Arr[i+1]<<" : "<<decimal_Val[i]<<" : "<<page_Num[i]<<" : "<<page_State[i]<<endl;
    // }

    // for(int i=0; i<decimal_Val.size(); i++){
    //     cout<<mem_Arr[i+1]<<" : "<<decimal_Val[i]<<" : "<<page_Num[i]<<endl;
    // }

    // cout<<mem_Arr[frame_Number+1]<<endl;


    return 0;
}