#include <stdio.h>
#include <stdlib.h>
#include <iostream>

using namespace std;

//Dislay function, used to display output in desired form
void display1(int time, char s, char d, char via, int cost);
void display2(char s, char d, char via, int cost);

//Structure to store routing table
struct node
{
    unsigned dist[20];
    unsigned from[20];
}rt[10];	

int main(int argc, char** argv){

	FILE *config_file;  /* configuration file */
	FILE *changConfig_file;  /* configuration change file */
	config_file = fopen(argv[1], "r");

	    // error handling
	    if (config_file == NULL) {
	       fprintf(stderr,"Error:Unable to open %s\n", argv[1]);
	       return 0;
	    }
	    changConfig_file = fopen(argv[2], "r");
		if (changConfig_file == NULL) {
	       fprintf(stderr,"Error:Unable to open %s\n", argv[1]);
	       return 0;
	    }		

	    char s,d,c, a,str1, str2;
		int i,j,k,count, cost, time=0;

		/* Read in data */
	    str1=fgetc(config_file);
	    int num_nodes = atoi(&str1);
	    double inf = 1000;
		int dmat[20][20];
		char Router[num_nodes];

		//setting initial value in dmat to unlimited distance
		for(i=0;i<num_nodes;i++){	
            for(j=0;j<num_nodes;j++){
            	dmat[i][j]=inf;
            }
		}

        printf("#START  \n");  
		/// Extracting Router ID  	
	    for (int r = 0; r < num_nodes; ++r){
	    	fgetc(config_file);
	    	str2=fgetc(config_file);
	    	Router[r]=  str2;
		}

		// Extracting Link Info
		fgetc(config_file);
		a =	fgetc(config_file); // Referring to the number of links 
	    int num_links = atoi(&a);
	   	for(int l = 0; l < num_links; ++l){
			fgetc(config_file);
			s = fgetc(config_file); //Source
			fgetc(config_file);
			d = fgetc(config_file); //Distination
			fgetc(config_file);
			c = fgetc(config_file); //cost of the link
			cost  = atoi(&c);
			for(int i=0;i<num_nodes;i++){  	
				// save link cost in rt data structure
				if (s==Router[i]){	
					for(int j=0;j<num_nodes;j++){ 
						if (d==Router[j]){
						dmat[i][i]=0;
						rt[i].dist[j]=cost;
						rt[i].from[j]=j;
						//displaying 2 way link info
						display1(time, s, d, Router[rt[i].from[j]], cost);
						display1(time, d, s, Router[rt[j].from[i]], cost);
						}
		   			}
          		}
       		}
		}

		for(i=0;i<num_nodes;i++){	
            for(j=0;j<num_nodes;j++){
            	cout<< dmat[i][j] << " ";
            }
			cout<<endl;
		}

		printf("\n\n#INITIAL  \n");
		for(i=0;i<num_nodes;i++){	
    		for(j=0;j<num_nodes;j++){
				if(rt[i].dist[j]!=0){
        			display2(Router[i], Router[j], Router[rt[i].from[j]], rt[i].dist[j]);
				}
			}
		}

	//Updating the table
   	do{   
        count=0;
        for(i=0;i<num_nodes;i++){	
        	for(j=0;j<num_nodes;j++){	
				for(k=0;k<num_nodes;k++){
					//Finding minimum cost
					if(rt[i].dist[j]>dmat[i][k]+rt[k].dist[j]){
						rt[i].dist[j]=rt[i].dist[k]+rt[k].dist[j];
						rt[i].from[j]=k;
						count++;
					}
            	}
			}	
		}
    }while(count!=0);

        //Checking for link change info
		printf("\n\n#UPDATE %d\n",cost);
       	c=fgetc(changConfig_file);
	    int	c_link = atoi(&c);
		for(j=0;j<c_link;j++)
            { //Extracting link change infor from change config file
            fgetc(changConfig_file);
            s=fgetc(changConfig_file);
            fgetc(changConfig_file);
            d=fgetc(changConfig_file);
            fgetc(changConfig_file);
            c=fgetc(changConfig_file);
	    	cost = atoi(&c);
		for(int i=0;i<num_nodes;i++){	
        if (s==Router[i]){	
			for(int j=0;j<num_nodes;j++)
        { 
				if (d==Router[j]){	
		dmat[i][i]=0;
		rt[i].dist[j]=cost;
		rt[i].from[j]=j;
		//Display change in link 
		display1(time, s, d, Router[rt[i].from[j]], cost);
		display1(time, d, s, Router[rt[j].from[i]], cost);	
				}
			}
          }
    	}
    }
        do
        {   
        	count=0;
            for(i=0;i<num_nodes;i++){	
            for(j=0;j<num_nodes;j++){	
            for(k=0;k<num_nodes;k++){
                if(rt[i].dist[j]>dmat[i][k]+rt[k].dist[j])
                {
                    rt[i].dist[j]=rt[i].dist[k]+rt[k].dist[j];
                    rt[i].from[j]=k;
                    count++;
                }
            }}}
        }while(count!=0);
        //Displaying final route
        printf("\n\n#FINAL  \n");
	    for(i=0;i<num_nodes;i++){	
        for(j=0;j<num_nodes;j++){
			if(rt[i].dist[j]!=0){
            	display2(Router[i], Router[j], Router[rt[i].from[j]], rt[i].dist[j]);
			}
		}}
printf("\n\n");
	    return (0);
}
//Display1 and display2 functions are used to display link information at different time stamp.
//At the input, they take source id s, destination id d, intermidiate router id 'via', and link cost.

void display1(int time, char s, char d, char via, int cost){
			 printf("\nt=%d distance from %c to %c via %c is %d",time,s,d,via,cost);
}   

void display2(char s, char d, char via, int cost){
			 printf("\nRouter %c: %c is %d through %c ",s,d,cost,via);
} 
