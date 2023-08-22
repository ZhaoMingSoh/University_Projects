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
using namespace std;
/*void output(){    
    int i;    
    cout<<"name   arrival   end   ready   running   waiting"<<endl;    
    for(i=0; i<result.size(); i++){    

    }    cout<<endl;
}*/



class customer{
    public:
    customer(string id,int arrival_time,int priority,int age,int tickets){
        this->id=id;
        this->arrival_time=arrival_time;
        this->priority=priority;
        this->age=age;
        this->tickets=tickets;
        run=0;
        running= tickets*5;
        wait=false;
        waiting=0;
        ready=-1;
    };
    string get_id(){
        return id;
    };
    int get_arrival_time(){
        return arrival_time;
    };
    int get_priority(){
        return priority;
    };
    int get_age(){
        return age;
    };
    int get_tickets(){
        return tickets;
    }
    int get_end(){
        return end;
    }
    int get_ready(){
        return ready;
    }
    int get_running(){
        return running;
    }
    int get_waiting(){
        return waiting;
    }
    bool get_wait(){
        return wait;
    }

    void change_age(int age){
        this->age=age;
    }
    void change_wait(){
        wait=true;
    }
    void change_back_wait(){
        wait=false;
    }

    void change_ticket(int tickets){
        this->tickets=tickets;
    }
    void change_ready(int ready){
        this->ready=ready;
    }
    void change_end(int end){
        this->end=end;
    }
    void change_waiting(int waiting){
        this->waiting=waiting;
    }
    void change_priority(int priority){
        this->priority=priority;
    }
    
    int start;
    
    
    int run ;
    private:
    string id;
    int arrival_time;
    int priority;
    int age;
    int tickets;
    int end;
    int ready;
    int running;
    int waiting;
    bool wait;
};





void sort_customer(vector<customer> &sort){
    int i,key,j;
    for(i=1;i<sort.size();i++){
        key=sort[i].get_priority();
        j=i-1;
        //sort priority
        while(j>=0 && sort[j].get_priority()>key){
            swap(sort[j+1],sort[j]);
            j=j-1;            
        }
        //sort arrival_time
        while(j>=0 && sort[j].get_priority()==key){
            if(sort[j].get_arrival_time()>sort[j+1].get_arrival_time()){
                swap(sort[j+1],sort[j]);
                j=j-1;
            }else{
                break;
            }
            
        }
        //sort id
        while(j>0 && sort[j].get_priority()==key && sort[j].get_arrival_time()==sort[j+1].get_arrival_time()){
            if(stoi(sort[j].get_id().erase(0,1))>stoi(sort[j+1].get_id().erase(0,1))){
                swap(sort[j+1],sort[j]);
                j=j-1;
            }else{
                break;
            }
            
        }
    }
}

void sort_arrivaltime(vector<customer> &vc){
    int i,key,j;
    for(int i=1;i<vc.size();i++){
        key=vc[i].get_arrival_time();
        j=i-1;
        while(j>=0 && vc[j].get_arrival_time()>key){
            swap(vc[j+1],vc[j]);
            j=j-1;            
        }
        while(j>=0 && vc[j].get_arrival_time()==key){
            if(vc[j].get_tickets()>vc[j+1].get_tickets()){
                swap(vc[j+1],vc[j]);
                j=j-1;
            }else{
                break;
            }
        }

    }

}

void sort_tickets(vector<customer> &vc){
    int i,key,j;
    for(int i=1;i<vc.size();i++){
        key=vc[i].get_tickets();
        j=i-1;
        while(j>=0 && vc[j].get_tickets()>key){
            swap(vc[j+1],vc[j]);
            j=j-1;            
        }
    }
}
bool interrupt(queue<customer> &process,customer obj){
    if(obj.get_tickets()<process.front().get_tickets()){
        return true;
    }else if(obj.get_tickets()==process.front().get_tickets()){
        //cout<<obj.get_id()<<'\t'<<"equal"<<'\t'<<process.front().get_id()<<endl;
    }
    return false;
}

void put_in_queue2(queue<customer> &process,vector<customer> &ready_queue,vector<customer> &obj,int time);
//
void put_into_normal(queue<customer> &process,vector<customer> &ready_queue,vector<customer> &obj,int &time){
    if(!process.empty()){
        ready_queue.push_back(obj[0]);
        sort_tickets(ready_queue);
        obj.erase(obj.begin());
        
    }else{
        if(ready_queue.size()!=0){
            ready_queue.push_back(obj[0]);
            obj.erase(obj.begin());
            sort_tickets(ready_queue);
            process.push(ready_queue[0]);
            ready_queue.erase(ready_queue.begin());
        }else{
            if(time<obj[0].get_arrival_time()){
                time=obj[0].get_arrival_time();
            }
            process.push(obj[0]);
            obj.erase(obj.begin());

        }
        
    }
    //cout<<obj[0].get_id()<<'\t'<<obj[0].get_arrival_time()<<'\t'<<time<<endl;
    
    if(obj.size()!=0){
        //cout<<"ok"<<endl;
        if(obj[0].get_arrival_time()==time){
            //cout<<"ok"<<endl;
            if(interrupt(process,obj[0])){
                //cout<<"put "<<obj[0].get_id()<<" with interrupt at :"<<time<<endl;
                put_in_queue2(process,ready_queue,obj,time);
            }else{
                //cout<<"put "<<obj[0].get_id()<<" without interrupt at :"<<time<<endl;
                put_into_normal(process,ready_queue,obj,time);
            }
        }
    }
}

void put_in_queue2(queue<customer> &process,vector<customer> &ready_queue,vector<customer> &obj,int time){
    customer front=process.front();
    process.pop();
    process.push(obj[0]);
    obj.erase(obj.begin());
    ready_queue.push_back(front);
    sort_tickets(ready_queue);
    if(obj.size()!=0){

    
        if(obj[0].get_arrival_time()==time){
            //cout<<"ok"<<endl;;
            if(interrupt(process,obj[0])){
                //cout<<"put "<<obj[0].get_id()<<" with interrupt at :"<<time<<endl;
                put_in_queue2(process,ready_queue,obj,time);
                
            }else{
                //cout<<"put "<<obj[0].get_id()<<" without interrupt at :"<<time<<endl;
                put_into_normal(process,ready_queue,obj,time);
            }
        }
    }

}
void sort_priority(vector<customer> &vc){
    int i,key,j;
    for(int i=1;i<vc.size();i++){
        key=vc[i].get_priority();
        j=i-1;
        while(j>=0 && vc[j].get_priority()>key){
            swap(vc[j+1],vc[j]);
            j=j-1;            
        }
    }
}

void sort_queue_priority(queue<customer> &process){
    vector<customer> copy;
    while(!process.empty()){
        copy.push_back(process.front());
        process.pop();
    }
    sort_priority(copy);
    for(int i=0;i<copy.size();i++){
        process.push(copy[i]);
    }
    
}
void sort_time(vector<customer> &vc){
    int i,key,j;
    for(int i=1;i<vc.size();i++){
        key=vc[i].get_arrival_time();
        j=i-1;
        while(j>=0 && vc[j].get_arrival_time()>key){
            swap(vc[j+1],vc[j]);
            j=j-1;            
        }
    }

}

void sort_except_process(queue<customer> &ready_queue){
    customer process=ready_queue.front();
    ready_queue.pop();
    vector<customer> copy;
    while(!ready_queue.empty()){
        copy.push_back(ready_queue.front());
        ready_queue.pop();
    }
    sort_priority(copy);
    ready_queue.push(process);
    for(int i=0;i<copy.size();i++){
        ready_queue.push(copy[i]);
    }
}
void sort_age(vector<customer> &vc){

    int i,key,j;
    for(int i=1;i<vc.size();i++){
        key=vc[i].get_age();
        j=i-1;
        while(j>=0 && vc[j].get_age()<key){
            //cout<<"swap"<<endl;
            swap(vc[i],vc[j]);
            j=j-1;            
        }
    }

}

void process_queue1(queue<customer> &ready_queue,vector<customer> &queue1 ,queue<customer> &queue2_ready_queue,vector<customer> &queue2,queue<customer> &result_queue ,vector<customer> &ready_queue2,int &time);

void queue2_while_loop(queue<customer> &ready_queue,vector<customer> &queue1 ,queue<customer> &queue2_ready_queue,vector<customer> &queue2,queue<customer> &result_queue ,vector<customer> &ready_queue2,int &time){
     while(!queue2_ready_queue.empty()){
        queue2_ready_queue.front().change_age(0);
        //cout<<"ok"<<endl;
        if(queue2_ready_queue.front().run==0 && queue2_ready_queue.front().get_ready()==-1){
            queue2_ready_queue.front().change_ready(time);
            //cout<<queue2_ready_queue.front().get_id()<<" ready at "<<time<<endl;
            //cout<<queue2_ready_queue.front().get_ready()<<endl;
        }else{
            if(queue2_ready_queue.front().get_wait()==true){
                    
                queue2_ready_queue.front().change_waiting(queue2_ready_queue.front().get_waiting()+(time-queue2_ready_queue.front().start));
                //cout<<queue2_ready_queue.front().get_id()<<" end at: "<<time<<endl;
                queue2_ready_queue.front().change_back_wait();
            }
        }
        queue2_ready_queue.front().run++;
        //cout<<"ok"<<endl;
        for(int i=0;i<queue2_ready_queue.front().get_tickets();i++){
            time+=5;
            queue2_ready_queue.front().change_ticket(queue2_ready_queue.front().get_tickets()-1);
            
            if(queue1.size()!=0){
                sort_time(queue1);
                if(time>=queue1[0].get_arrival_time()){
                    ready_queue.push(queue1[0]);
                    queue1.erase(queue1.begin());

                    queue2_ready_queue.front().start=time;
                    queue2_ready_queue.front().change_wait();
                    //cout<<queue2_ready_queue.front().get_id()<<" wait start at "<<time<<endl;
                    ready_queue2.push_back(queue2_ready_queue.front());
                    sort_tickets(ready_queue2);
                    queue2_ready_queue.pop();
                    process_queue1(ready_queue,queue1,queue2_ready_queue,queue2,result_queue,ready_queue2,time);
                }
            }

            for(int i=0;i<ready_queue2.size();i++){
                ready_queue2[i].change_age(ready_queue2[i].get_age()+5);
                if(ready_queue2[i].get_age()>=100){
                    ready_queue2[i].change_priority(ready_queue2[i].get_priority()-1);
                    ready_queue2[i].change_age(ready_queue2[i].get_age()-100);
                    //cout<<ready_queue2[i].get_id()<<'\t'<<ready_queue2[i].get_priority()<<'\t'<<"promote"<<endl;
                    //cout<<ready_queue2.size()<<endl;
                    if(ready_queue2[i].get_priority()<4){
                        //cout<<ready_queue2[i].get_id()<<'\t'<<ready_queue2[i].get_priority()<<'\t'<<"to queue1"<<endl;
                        ready_queue2[i].change_age(0);
                        ready_queue2[i].run=0;
                        ready_queue.push(ready_queue2[i]);

                        //cout<<"promote to queue1 :"<<ready_queue2[i].get_id()<<" at: "<<time<<endl;

                        ready_queue2.erase(ready_queue2.begin()+i);
                        
                        queue2_ready_queue.front().start=time;
                        queue2_ready_queue.front().change_wait();
                        ready_queue2.push_back(queue2_ready_queue.front());
                        queue2_ready_queue.pop();

                        process_queue1(ready_queue,queue1,queue2_ready_queue,queue2,result_queue,ready_queue2,time);
                        if(ready_queue.empty() && queue1.size()==0 && queue2_ready_queue.empty() && queue2.size()==0 && ready_queue2.size()==0){
                            //cout<<"ok"<<endl;
                            //return ; 
                            break; 
                        }else{
                            //cout<<"still left "<<endl;
                        }
                    }
                }
            }
            if(ready_queue.empty() && queue1.size()==0 && queue2_ready_queue.empty() && queue2.size()==0 && ready_queue2.size()==0){
                //cout<<"ok"<<endl;
                //return ; 
                break; 
            }
            
            //cout<<"ok"<<endl;
            if(queue2.size()!=0){
                if(queue2[0].get_arrival_time()==time){
                    //cout<<time<<endl;
                    if(interrupt(queue2_ready_queue,queue2[0])){
                        //cout<<"interrupt"<<endl;
                        if(queue2_ready_queue.front().get_wait()==false){
                            queue2_ready_queue.front().change_wait();
                            queue2_ready_queue.front().start=time;
                        }
                        //cout<<"put "<<queue2[0].get_id()<<" with interrupt at :"<<time<<endl;        
                        put_in_queue2(queue2_ready_queue,ready_queue2,queue2,time);
                        queue2_while_loop(ready_queue,queue1,queue2_ready_queue,queue2,result_queue,ready_queue2,time);
                    }else{
                        //cout<<"normal"<<endl;
                        //cout<<"put "<<queue2[0].get_id()<<" without interrupt at :"<<time<<endl; 
                        put_into_normal(queue2_ready_queue,ready_queue2,queue2,time);
                        //cout<<queue2[0].get_id()<<endl;
                                
                    }
                }
            }
            
            

        }
        /*if(time==90){
            cout<<queue2_ready_queue.front().get_id()<<endl;
        }*/
        if(ready_queue.empty() && queue1.size()==0 && queue2_ready_queue.empty() && queue2.size()==0 && ready_queue2.size()==0){
            //cout<<"ok"<<endl;
            //return ; 
            //break; 
        }else{
            if(queue2_ready_queue.front().get_tickets()==0){
            //cout<<"ok"<<endl;
            //cout<<time<<endl;
            //cout<<queue2_ready_queue.front().get_id()<<" end at "<<time<<endl;
            queue2_ready_queue.front().change_end(time);
            result_queue.push(queue2_ready_queue.front());
            queue2_ready_queue.pop();
            if(ready_queue2.size()!=0){
                queue2_ready_queue.push(ready_queue2[0]);
                ready_queue2.erase(ready_queue2.begin());
            }else{
                        
            }
                    
            }
        }
        //cout<<"ok"<<endl;
        


    }
}
void process_queue2(queue<customer> &ready_queue,vector<customer> &queue1 ,queue<customer> &queue2_ready_queue,vector<customer> &queue2,queue<customer> &result_queue ,vector<customer> &ready_queue2,int &time);
void process_queue1(queue<customer> &ready_queue,vector<customer> &queue1 ,queue<customer> &queue2_ready_queue,vector<customer> &queue2,queue<customer> &result_queue ,vector<customer> &ready_queue2,int &time){
    //queue 1 not empty;
    //cout<<"ok"<<endl;
    if(ready_queue.empty() && time ==0 && queue1.size()!=0){
        sort_time(queue1);
        time=queue1[0].get_arrival_time();
        //cout<<time<<endl;
        sort_customer(queue1);
        for(int i=0;i<queue2.size();i++){
            if(queue2[i].get_arrival_time()<=time){
                //cout<<"push "<<queue2[0].get_id()<<" into queue2 ready queue at "<<time<<endl;
                ready_queue2.push_back(queue2[0]);
                queue2.erase(queue2.begin());
                if(i>=0){
                    i=i-1;
                }
            }
            if(time<queue2[0].get_arrival_time() || queue2.size()==0){
                break;
            }
        }

    }
   
    //push first element
    if(ready_queue.empty() && queue1.size()!=0 ){
        sort_time(queue1);
        for(int i=0;i<queue1.size();i++){
            if(queue1[i].get_arrival_time()<=time){
                ready_queue.push(queue1[0]);
                //cout<<"Push "<<queue1[0].get_id()<<" at "<<time<<endl;
                /*for(int j=0;j<queue1.size();j++){
                    if(arrival_time[0].get_id()==queue1[j].get_id()){
                        queue1.erase(queue1.begin()+i);
                        break;
                    }
                }*/
                queue1.erase(queue1.begin());
                if(i>=0){
                    i=i-1;
                }
            }
            if(time<queue1[0].get_arrival_time() || queue1.size()==0){
                break;
            }
        }
        
    }
    sort_customer(queue1);
    
    //cout<<"ok"<<endl;
    //run until queue 1 is empty
    //queue1
    while(!ready_queue.empty()){
        //tickets != 0
        while(queue2.size()!=0){
            if(queue2[0].get_arrival_time()<=time){
                if(queue2[0].get_arrival_time() <time){
                    queue2[0].change_age( time-queue2[0].get_arrival_time());
                }
                ready_queue2.push_back(queue2[0]);
                //cout<<"Put "<<queue2[0].get_id()<<" into queue2 ready queue at "<<time<<" with age "<<queue2[0].get_age()<<endl;
                queue2.erase(queue2.begin());
                
            }else{
                break;
            }
        }

        if(ready_queue.front().get_tickets()!=0){
            //first run or not 
            if(ready_queue.front().run==0 && ready_queue.front().get_ready() ==-1){
                //cout<<ready_queue.front().get_id()<<" ready at "<<time<<endl;
                ready_queue.front().change_ready(time);
            }else{
                
                //cout<<ready_queue.front().get_wait()<<endl;
                if(ready_queue.front().get_wait()==true){
                    
                    ready_queue.front().change_waiting(ready_queue.front().get_waiting()+(time-ready_queue.front().start));
                    //cout<<ready_queue.front().get_id()<<" waiting time end at "<<time<<endl;
                    ready_queue.front().change_back_wait();
                }
            }
            
            
            /*
            if(ready_queue.front().get_id()=="a1"){
                cout<<ready_queue.front().get_tickets()<<"\t"<<ready_queue.front().get_priority()<<'\t'<<ready_queue.front().run<<endl;
            }*/
            
            //calculate N
            int N=((10-ready_queue.front().get_priority())*10)/5;
            
            
            //can be solved
            if(ready_queue.front().get_tickets()<=N){
                //cout<<"ok"<<endl;
                //time passed
                
                
                time+=ready_queue.front().get_tickets()*5;
                /*
               for(int i=0;i<queue1.size();i++){
                    if(time >=queue1[i].get_arrival_time()){
                        ready_queue.push(queue1[i]);
                        cout<<"push "<<queue1[i].get_id()<<" at "<<time<<endl;
                        queue1.erase(queue1.begin());
                        //cout<<"next is : "<<queue1[i].get_id()<<" with arrival time "<<queue1[i].get_arrival_time()<<endl;
                        if(i>=0){
                            i=i-1;
                        }
                    }
                    if(time<queue1[0].get_arrival_time() || queue1.size()==0){
                        break;
                    }
                }*/
                sort_time(queue1);
                while(queue1.size()!=0){
                    if(queue1[0].get_arrival_time()<=time){
                    
                        ready_queue.push(queue1[0]);
                        //cout<<"push "<<queue1[0].get_id()<<" at "<<time<<endl;
                        queue1.erase(queue1.begin());
                        sort_except_process(ready_queue);
                    }else{
                        break;
                    }
                }
                sort_customer(queue1);
                
                //ready_queue.front().change_ticket(0);
                //set end;
                vector<customer> promote_list;
                for(int i=0;i<ready_queue2.size();i++){
                    
                    ready_queue2[i].change_age(ready_queue2[i].get_age()+ready_queue.front().get_tickets()*5);
                    
                    if(ready_queue2[i].get_age()>=100){
                        ready_queue2[i].change_priority(ready_queue2[i].get_priority()-(ready_queue2[i].get_age()/100));
                        ready_queue2[i].change_age(ready_queue2[i].get_age()%100);
                        if(ready_queue2[i].get_priority()<4){
                            
                            promote_list.push_back(ready_queue2[i]);
                            //cout<<"promote:"<<ready_queue2[i].get_id()<<" at: "<<time<<endl;
                            /*ready_queue2[i].run=0;
                            ready_queue.push(ready_queue2[i]);*/
                            
                            ready_queue2.erase(ready_queue2.begin()+i);
                            if(i>=0){
                                i=i-1;
                            }
                            
                        }
                    }
                }
                sort_age(promote_list);
                while(promote_list.size()!=0){
                    
                    //cout<<"promote:"<<promote_list[0].get_id()<<" at: "<<time<<" with age "<<promote_list[0].get_age()<<endl;
                    promote_list[0].run=0;
                    ready_queue.push(promote_list[0]);
                    promote_list.erase(promote_list.begin());
                }
                
                
                ready_queue.front().change_end(time);
                //cout<<ready_queue.front().get_id()<<" end at "<<time<<endl;
                result_queue.push(ready_queue.front());
                
                
                ready_queue.pop();
               
            }
            //cant be solved
            //1. solve max ticket;
            //2. put it at the end of queue;
            //3. waiting time start;
            //4. add time to queue2 ready queue age;
            else{
                //run ++
                ready_queue.front().run++;
                
                //time comsuption
                time+=N*5;
                
                /*
                for(int i=0;i<queue1.size();i++){
                    if(time >=queue1[i].get_arrival_time()){
                        ready_queue.push(queue1[i]);
                        cout<<"push "<<queue1[i].get_id()<<" at "<<time<<endl;
                        queue1.erase(queue1.begin());
                        //cout<<"next is : "<<queue1[i].get_id()<<" with arrival time "<<queue1[i].get_arrival_time()<<endl;
                        if(i>=0){
                            i=i-1;
                        }
                    }
                    if(time<queue1[0].get_arrival_time() || queue1.size()==0){
                        break;
                    }
                }*/
                sort_time(queue1);
                while(queue1.size()!=0){
                    if(queue1[0].get_arrival_time()<=time){
                    
                        ready_queue.push(queue1[0]);
                        //cout<<"push "<<queue1[0].get_id()<<" at "<<time<<endl;
                        queue1.erase(queue1.begin());
                        sort_except_process(ready_queue);
                    }else{
                        break;
                    }
                }
                sort_customer(queue1);
                
                
                
                if(ready_queue.front().get_wait()==false){
                    ready_queue.front().change_wait();
                    ready_queue.front().start=time;
                    //cout<<ready_queue.front().get_id()<<" waitting time start at "<<time<<endl;
                    //cout<<ready_queue.front().get_wait()<<endl;
                    //cout<<ready_queue.front().start<<endl;
                }
                ready_queue.front().change_ticket(ready_queue.front().get_tickets()-N);
                //
                
                /*if(ready_queue.front().get_id()=="a1"){
                    cout<<ready_queue.front().get_tickets()<<"\t"<<ready_queue.front().get_priority()<<endl;
                }*/
                /*if(time==1170){
                    cout<<"     "<<ready_queue.front().get_id()<<"     "<<ready_queue.front().run<<"   "<<ready_queue.front().get_priority()<<endl;
                }*/
                
                /*
                for(int i=0;i<ready_queue2.size();i++){
                    
                    ready_queue2[i].change_age(ready_queue2[i].get_age()+N*5);
                    if(ready_queue2[i].get_age()>=100){
                        ready_queue2[i].change_priority(ready_queue2[i].get_priority()-(ready_queue2[i].get_age()/100));
                        ready_queue2[i].change_age(ready_queue2[i].get_age()%100);
                        if(ready_queue2[i].get_priority()<4){
                            cout<<"promote:"<<ready_queue2[i].get_id()<<" at: "<<time<<endl;
                            ready_queue2[i].run=0;
                            ready_queue.push(ready_queue2[i]);
                            ready_queue2.erase(ready_queue2.begin()+i);
                            if(i>=0){
                                i=i-1;
                            }
                        }
                    }
                }*/
                

                

                if(ready_queue.front().run%2==0){
                    
                    ready_queue.front().change_priority(ready_queue.front().get_priority()+1);
                    
                    //priority >= 4
                    //1. put into queue 2
                    //2. wait time start
                    if(ready_queue.front().get_priority()>=4){
                        
                        vector<customer> promote_list;
                        for(int i=0;i<ready_queue2.size();i++){
                            
                            ready_queue2[i].change_age(ready_queue2[i].get_age()+N*5);
                            
                            if(ready_queue2[i].get_age()>=100){
                                ready_queue2[i].change_priority(ready_queue2[i].get_priority()-(ready_queue2[i].get_age()/100));
                                ready_queue2[i].change_age(ready_queue2[i].get_age()%100);
                                if(ready_queue2[i].get_priority()<4){
                                    
                                    promote_list.push_back(ready_queue2[i]);
                                    //cout<<"promote:"<<ready_queue2[i].get_id()<<" at: "<<time<<endl;
                                    /*ready_queue2[i].run=0;
                                    ready_queue.push(ready_queue2[i]);*/
                                    
                                    ready_queue2.erase(ready_queue2.begin()+i);
                                    if(i>=0){
                                        i=i-1;
                                    }
                                    
                                }
                            }
                        }
                        sort_age(promote_list);
                        while(promote_list.size()!=0){
                            
                            //cout<<"promote:"<<promote_list[0].get_id()<<" at: "<<time<<" with age "<<promote_list[0].get_age()<<endl;
                            promote_list[0].run=0;
                            promote_list[0].change_age(0);
                            ready_queue.push(promote_list[0]);
                            promote_list.erase(promote_list.begin());
                        }
                        
                        //cout<<ready_queue.front().get_id()<<'\t'<<ready_queue.front().get_tickets()<<'\t'<<ready_queue.front().get_priority()<<endl;
                        //cout<<"put "<<ready_queue.front().get_id()<<" into queue2 at "<<time<<endl;
                        
                        ready_queue.front().change_wait();
                        ready_queue.front().start=time;
                        ready_queue.front().change_age(0);
                        ready_queue2.push_back(ready_queue.front());
                        sort_tickets(ready_queue2);
                        ready_queue.pop();
                        //cout<<"next is "<<ready_queue.front().get_id()<<' '<<ready_queue.front().run<<" ticket: "<<ready_queue.front().get_tickets()<<endl;
                        if(ready_queue.empty()){
                            break;
                        }
                    }else{
                        vector<customer> promote_list;
                        for(int i=0;i<ready_queue2.size();i++){
                            
                            ready_queue2[i].change_age(ready_queue2[i].get_age()+N*5);
                            
                            if(ready_queue2[i].get_age()>=100){
                                ready_queue2[i].change_priority(ready_queue2[i].get_priority()-(ready_queue2[i].get_age()/100));
                                ready_queue2[i].change_age(ready_queue2[i].get_age()%100);
                                if(ready_queue2[i].get_priority()<4){
                                    
                                    promote_list.push_back(ready_queue2[i]);
                                    //cout<<"promote:"<<ready_queue2[i].get_id()<<" at: "<<time<<endl;
                                    /*ready_queue2[i].run=0;
                                    ready_queue.push(ready_queue2[i]);*/
                                    
                                    ready_queue2.erase(ready_queue2.begin()+i);
                                    if(i>=0){
                                        i=i-1;
                                    }
                                    
                                }
                            }
                        }
                        sort_age(promote_list);
                        while(promote_list.size()!=0){
                            
                            //cout<<"promote:"<<promote_list[0].get_id()<<" at: "<<time<<" with age "<<promote_list[0].get_age()<<endl;
                            promote_list[0].run=0;
                            promote_list[0].change_age(0);
                            ready_queue.push(promote_list[0]);
                            promote_list.erase(promote_list.begin());
                        }
                        customer current=ready_queue.front();
                        ready_queue.pop();
                        ready_queue.push(current);
                        sort_queue_priority(ready_queue);
                        
                    }
                    
                }else{
                    

                    customer current=ready_queue.front();
                    ready_queue.pop();
                    vector<customer> promote_list;
                    for(int i=0;i<ready_queue2.size();i++){
                            
                        ready_queue2[i].change_age(ready_queue2[i].get_age()+N*5);
                            
                        if(ready_queue2[i].get_age()>=100){
                            ready_queue2[i].change_priority(ready_queue2[i].get_priority()-(ready_queue2[i].get_age()/100));
                            ready_queue2[i].change_age(ready_queue2[i].get_age()%100);
                            if(ready_queue2[i].get_priority()<4){
                                
                                promote_list.push_back(ready_queue2[i]);
                                //cout<<"promote:"<<ready_queue2[i].get_id()<<" at: "<<time<<endl;
                                /*ready_queue2[i].run=0;
                                ready_queue.push(ready_queue2[i]);*/
                                    
                                ready_queue2.erase(ready_queue2.begin()+i);
                                if(i>=0){
                                    i=i-1;
                                }
                                
                            }
                        }
                    }
                    sort_age(promote_list);
                    while(promote_list.size()!=0){
                        //cout<<"promote:"<<promote_list[0].get_id()<<" at: "<<time<<" with age "<<promote_list[0].get_age()<<endl;
                        promote_list[0].run=0;
                        promote_list[0].change_age(0);
                        ready_queue.push(promote_list[0]);
                        promote_list.erase(promote_list.begin());
                    }
                    ready_queue.push(current);
                    sort_queue_priority(ready_queue);
                    
                }
                


                
            }

        }
        //ticket = 0; 
        //1. set end time;
        //2. pop ;
        else{
            ready_queue.front().change_end(time);
            result_queue.push(ready_queue.front());
            ready_queue.pop();
        }
        
    }
    if(!queue2_ready_queue.empty() || queue2.size()!=0 || ready_queue2.size() != 0){
        process_queue2(ready_queue,queue1,queue2_ready_queue,queue2,result_queue,ready_queue2,time);
    }

    if(queue1.size()!=0){
        process_queue1(ready_queue,queue1,queue2_ready_queue,queue2,result_queue,ready_queue2,time);
    }
}

void process_queue2(queue<customer> &ready_queue,vector<customer> &queue1 ,queue<customer> &queue2_ready_queue,vector<customer> &queue2,queue<customer> &result_queue ,vector<customer> &ready_queue2,int &time){
    if(time==0){
        if(queue2.size()!=0){
            sort_arrivaltime(queue2);
            time=queue2[0].get_arrival_time();
        }
    }
    
    for(int i=0;i<queue2.size();i++){
        if(queue2[i].get_arrival_time()<=time){
            ready_queue2.push_back(queue2[i]);
            queue2.erase(queue2.begin()+i);
            if(i>=0){
                i=i-1;
            }
        }
    }
    
    if(ready_queue2.size()!=0){
        sort_tickets(ready_queue2);
    
        //cout<<ready_queue2.size()<<endl;
        for(int i=0;i<ready_queue2.size();i++){
            //cout<<"queue2 left: "<<ready_queue2[i].get_id()<<" with ticket "<<ready_queue2[i].get_tickets()<<endl;
        }
    
        queue2_ready_queue.push(ready_queue2[0]);
        ready_queue2.erase(ready_queue2.begin());
    }
    
    //cout<<ready_queue2.size()<<endl;
    queue2_while_loop(ready_queue,queue1,queue2_ready_queue,queue2,result_queue,ready_queue2,time);
    
    if(ready_queue.empty() && queue1.size()==0 && queue2_ready_queue.empty() && queue2.size()==0 && ready_queue2.size()==0){
        //cout<<"ok"<<endl;
        //return ;  
    }else{
        if(queue1.size()!=0){
            if(queue2.size()!=0){
                sort_time(queue1);
                int T=queue1[0].get_arrival_time();
                sort_customer(queue1);
                if(queue2[0].get_arrival_time()<T){
                    time=queue2[0].get_arrival_time();
                    process_queue2(ready_queue,queue1,queue2_ready_queue,queue2,result_queue,ready_queue2,time);
                }else{
                    time=T;
                    process_queue1(ready_queue,queue1,queue2_ready_queue,queue2,result_queue,ready_queue2,time);
                }
            }else{
                sort_time(queue1);
                int T=queue1[0].get_arrival_time();
                sort_customer(queue1);
                time=T;
                process_queue1(ready_queue,queue1,queue2_ready_queue,queue2,result_queue,ready_queue2,time);
            }
        }else{
            if(queue2.size()!=0){
                time=queue2[0].get_arrival_time();
                process_queue2(ready_queue,queue1,queue2_ready_queue,queue2,result_queue,ready_queue2,time);
            }
        }
    }
}

void process(queue<customer> &ready_queue,vector<customer> &queue1 ,queue<customer> &queue2_ready_queue,vector<customer> &queue2,queue<customer> &result_queue ,vector<customer> &ready_queue2,int &time){
    
    
    if(queue1.size()!=0){
        //cout<<"ok"<<endl;
        sort_time(queue1);
        int T =queue1[0].get_arrival_time();
        sort_customer(queue1);
        if(queue2.size()!=0){
            if(T<=queue2[0].get_arrival_time()){
                //cout<<"ok"<<endl;
                process_queue1(ready_queue,queue1,queue2_ready_queue,queue2,result_queue,ready_queue2,time);
            }else{
                process_queue2(ready_queue,queue1,queue2_ready_queue,queue2,result_queue,ready_queue2,time);
            }
        }else{
            process_queue1(ready_queue,queue1,queue2_ready_queue,queue2,result_queue,ready_queue2,time);
        }
        
    }else{
        process_queue2(ready_queue,queue1,queue2_ready_queue,queue2,result_queue,ready_queue2,time);
    }
    
    
    //cout<<time<<endl;
    /*for(int i=0;i<ready_queue2.size();i++){
        cout<<ready_queue2[i].get_id()<<'\t'<<ready_queue2[i].get_tickets()<<'\t'<<ready_queue2[i].get_priority()<<endl;
    }*/
    
    
    //cout<<"ok"<<endl;
    
    

    
    

}


int main(){
    vector<customer> Customer;
    vector<customer> queue1;
    vector<customer> queue2;
    string Input_line;
    ifstream myfile("input.txt");

    string Id;
    int Arrival_time,Priority,Age,Tickets;

    if (myfile.is_open()){
        while ( getline (myfile,Input_line) ){
            stringstream input(Input_line);
            //input.push_back(Input_line);
            input >> Id >> Arrival_time >> Priority >> Age >>Tickets;
            customer a=customer(Id,Arrival_time,Priority,Age,Tickets);
            Customer.push_back(a);
        }
        myfile.close();
    }else cout << "Unable to open file"; 

    for(int i=0;i<Customer.size();i++){
        if(Customer[i].get_priority()<4){
            queue1.push_back(Customer[i]);
        }else{
            queue2.push_back(Customer[i]);
        }
    }
    sort_customer(queue1);
    sort_arrivaltime(queue2);
    //sort_arrivaltime(queue2);
    /*for(int i=0;i<queue2.size();i++){
        cout<<queue2[i].get_id()<<endl;
    }*/

    /*for(int i=0;i<queue1.size();i++){
        cout<<queue1[i].get_id()<<' '<<queue1[i].get_arrival_time()<<' '<<queue1[i].get_priority()<<' '<<queue1[i].get_age()<<' '<<queue1[i].get_tickets()<<endl;
    }*/
    vector<customer> ready_queue2;
    queue<customer> ready_queue;
    queue<customer> result_queue;
    queue<customer> queue2_ready_queue;
    /*for(int i=0;i<queue1.size();i++){
        ready_queue.push(queue1[i]);
    }*/
    
    int time=0;
    process(ready_queue,queue1,queue2_ready_queue,queue2,result_queue,ready_queue2,time);
    cout<<"name"<<'\t'<<"arrival"<<'\t'<<"end"<<'\t'<<"ready"<<'\t'<<"running"<<'\t'<<"waiting"<<endl;
    while(!result_queue.empty()){
        
        cout<<result_queue.front().get_id()<<'\t'<<result_queue.front().get_arrival_time()<<'\t'<<result_queue.front().get_end()<<'\t'<<result_queue.front().get_ready()<<'\t'<<result_queue.front().get_running()<<'\t'<<result_queue.front().get_waiting()<<endl;

        result_queue.pop();
    }
    
    
    

}


