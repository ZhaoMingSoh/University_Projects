#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#define SIZE 26

using namespace std;

// Calculate the appropriate hash key value for each of the given key
int hash_key(string key){
    char temp = key[key.length()-1];    // store the last character of each given key
    int index = 0;

    // Give each character its appropriate hash_key value == index of the hash table
    if(temp == 'a'){
        index = 0;
    }
    else if(temp == 'b'){
        index = 1;
    }
    else if(temp == 'c'){
        index = 2;
    }
    else if(temp == 'd'){
        index = 3;
    }
    else if(temp == 'e'){
        index = 4;
    }
    else if(temp == 'f'){
        index = 5;
    }
    else if(temp == 'g'){
        index = 6;
    }
    else if(temp == 'h'){
        index = 7;
    }
    else if(temp == 'i'){
        index = 8;
    }
    else if(temp == 'j'){
        index = 9;
    }
    else if(temp == 'k'){
        index = 10;
    }
    else if(temp == 'l'){
        index = 11;
    }
    else if(temp == 'm'){
        index = 12;
    }
    else if(temp == 'n'){
        index = 13;
    }
    else if(temp == 'o'){
        index = 14;
    }
    else if(temp == 'p'){
        index = 15;
    }
    else if(temp == 'q'){
        index = 16;
    }
    else if(temp == 'r'){
        index = 17;
    }
    else if(temp == 's'){
        index = 18;
    }
    else if(temp == 't'){
        index = 19;
    }
    else if(temp == 'u'){
        index = 20;
    }
    else if(temp == 'v'){
        index = 21;
    }
    else if(temp == 'w'){
        index = 22;
    }
    else if(temp == 'x'){
        index = 23;
    }
    else if(temp == 'y'){
        index = 24;
    }
    else if(temp == 'z'){
        index = 25;
    }

    return index % SIZE; // return the given key index 
    
}

// Linear probing of the hash table
int probe(string H[], string Status[], string key){
    int index = hash_key(key);  

    // If the Status entry for the given index is not "never used" then keep on looping until
    while(Status[index] != "never used"){
        if(H[index] == key){    // either the key is already in the Hash table
            break;              // exit the loop
        }
        else if(H[index] != key || Status[index] == "tombstone"){   // the key is not in the Hash table or the Status entry for the given index is a "tombstone" == suggesting that element was there but deleted
            index = (index + 1)%SIZE;   // The modulo here is to ensure that it can wrap around the Hash table entry 
        }                               // For example : index = 26 % 26 = 0 (Starts from the first entry of the Hash table)
    }

    return index;
}

// Insert a new key into the Hash table
void insert(string H[], string Status[], string key){
    int index = hash_key(key);
    int n = 0;

    while(Status[index] == "occupied"){
        if(H[index] == key){
            break;
        }
        index = (index+1)%SIZE;
        n++;
        if(n == SIZE){
            break;
        }
    }

    while(Status[index] == "never used" || Status[index] == "tombstone"){
        H[index] = key;
        Status[index] = "occupied";
    }

    /*// If the Status entry for the given index of the key is occupied
    // There are 3 possibilities : either the new key is already in the Hash table or the key at the current index is not equal to the new key or it is empty (deleted key)
    if(Status[index] == "occupied"){
        index = probe(H, Status, key);  // use the linear probing function to check for the possibilities
    }
    
    // If the Status entry for the given index is either "never used" or "tombstone" then put the key into the Hash table entry
    H[index] = key;
    Status[index] = "occupied";*/

}

void delete_(string H[], string Status[], string key){

   int index = hash_key(key);
    int n = 0;
    
    while(Status[index] == "tombstone" || Status[index] == "occupied"){
        if(H[index] == key){
            H[index] = "";
            Status[index] = "tombstone";
        }
        index = (index+1)%SIZE;
        n++;
        if(n == SIZE){
            break;
        }
    }
    /*int index = hash_key(key);

    if(Status[index] == "occupied"){
        index = probe(H, Status, key);
    }

    H[index] = "";
    Status[index] = "tombstone";*/

    /*int fix_index = 0;
    while(index != fix_index){
        fix_index = index + 1;
        if(Status[fix_index] == "never used" || Status[fix_index] == "tombstone"){
            return;
        }
        if(hash_key(H[fix_index]) > index ){
            fix_index++;
        }
        else{
            H[index] = H[fix_index];
            Status[fix_index] = "tombstone";
            index = fix_index;
        }
    }*/
    /*int index = hash_key(key);

    if(Status[index] == "occupied"){
        int index = probe(H, Status, key);
    }

    Status[index] = "tombstone";
    H[index] = "";
    int fix_index = index + 1;

    while(index != fix_index){
        repair:
        if(H[fix_index] == "never used" || H[fix_index] == "tombstone"){
            break;
        }
        if(hash_key(H[fix_index]) > index){
            fix_index = (fix_index + 1) % SIZE;
            goto repair;
        }
        else{
            H[index] = H[fix_index];
            Status[fix_index] = "tombstone";
            index = fix_index;
        }
    }*/
}


int main(){
    string Hash_Table[26];  
    string Status_Table[26];

    for(int i = 0; i < 26; i++){
        Status_Table[i] = "never used";
    }

    string Input, temp;
    vector<string> capture;
    vector<string> final;

    getline(cin, Input);

    istringstream iss(Input);   // Place the entire Input string into the string stream 
    for(string Input; iss >> Input;){   // Place each and every elements separated by space/whitespace into the "capture" vector
        capture.push_back(Input);
    }

    // Calling the insert() and delete_() for each of the given Input 
    for(int i = 0; i < capture.size(); i++){
        if(capture[i][0] == 'A'){
            temp = capture[i].substr(1);   
            insert(Hash_Table, Status_Table, temp);
        }
        if(capture[i][0] == 'D'){
            temp = capture[i].substr(1);
            delete_(Hash_Table, Status_Table, temp);
        }
    }

    for(int i = 0; i < 26; i++){
        if(Hash_Table[i] == ""){ // skip over the empty entries
        }
        else{
            final.push_back(Hash_Table[i]); // Place all the non-empty entries element into the "final" vector
        }
    }
    
    // Output the corresponding Hash_table non-empty elements 
    for(int i = 0; i < final.size(); i++){
        cout<<final[i]<<" ";
    }
    cout<<endl;

    for(int i = 0; i < SIZE; i++){
        cout<<Status_Table[i]<<endl;
    }

   
    return 0;
}

