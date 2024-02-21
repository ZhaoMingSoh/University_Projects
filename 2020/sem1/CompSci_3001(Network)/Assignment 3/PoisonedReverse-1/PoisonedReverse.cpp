#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "PoisonedReverse.h"
#include "Router.h"

#define POISON_REVERSE              // uncomment to use Poisoned Reverse

// ---------------------------------

int     num_nodes;                  // number of routers/nodes in the topology
int     time;

CRouter Routers[max_size];

char cost_str[16];
char* cost_view(int cost)           // prints "Inf" if cost value is infinity
{
    if (cost >= inf)
        sprintf(cost_str, "Inf");
    else
        sprintf(cost_str, "%d", cost);
    return  cost_str;
}


void print_dt(int x)                // prints Distance table and Routing table for router X
{

    printf("\n\nD[%c]", Routers[x].get_id());
    for (int i = 0; i < CRouter::count; ++i)
        if (x != i)
            printf(" %3c", Routers[i].get_id());
    printf("%16s","Route");
    for (int i = 0; i < CRouter::count; ++i)
    {
        if (x == i)
            continue;
        printf("\n %3c", Routers[i].get_id());
        for (int j = 0; j < CRouter::count; ++j)
            if (x != j)
                printf(" %3s", cost_view(Routers[x].dt[i][j]));

        printf("%16s via %c", cost_view(Routers[x].getCost(i)),
            Routers[x].getRout(i) >= 0 ? Routers[Routers[x].getRout(i)].get_id() : '-');
    }
}

void print_all()
{
    return; // comment out this line to show details
    printf("\n\n-------------- Time=%d --------------", time);
    for (int i = 0; i < num_nodes; i++)
        print_dt(i);
}


// ---------------------------------
// Display1 and display2 functions are used to display link information at different time stamp.
// At the input, they take source id s, destination id d, intermidiate router id 'via', and link cost.

void display1(int time, char s, char d, char via, int cost)
{
    printf("\nt=%d distance from %c to %c via %c is %s", time, s, d, via, cost_view(cost));
}

void display2(char s, char d, char via, int cost)
{
    printf("\nRouter %c: %c is %s routing through %c ", s, d, cost_view(cost), via);
}

void display_all()
{
    for (int i = 0; i < num_nodes; i++)
    {
        for (int j = 0; j < num_nodes; j++)
            if (Routers[i].getCost(j) != 0)
                display2(Routers[i].get_id(), Routers[j].get_id(), Routers[Routers[i].getRout(j)].get_id(), Routers[i].getCost(j));
        printf("\n");
    }
}

// ---------------------------------

int get_index(char x)
{
    int i;
    for(i=0;x!=Routers[i].get_id();++i);
    return i;
}

// ---------------------------------

void update_table()                             // Updating the table
{
    int count;
    do
    {
        ++time;
        CRouter Routers_pre[max_size];
        memcpy(Routers_pre, Routers, sizeof(Routers_pre));  // store previous state of table
        count = 0;
        //printf("\n");

        for (int i = 0; i < num_nodes; i++)
        {
            bool printed = false;
            for (int j = 0; j < num_nodes; j++)
                for (int k = 0; k < num_nodes; k++)
                {
                    unsigned int cost_via_k = Routers_pre[i].ndt[k] + Routers_pre[k].getCost(j);
                    // In this code, when Poison Reverse is enabled (#ifdef POISON_REVERSE), if router i is a neighbor of router k, and the destination j was previously routed through i, the cost (cost_via_k) is set to infinity (inf). This prevents the route from being used during the update, helping to break the loop.
#ifdef POISON_REVERSE
                    if (Routers[i].neighbours[k] && (i!=j))
                    if (Routers_pre[k].getRout(j) == i)
                        cost_via_k = inf;
#endif // POISON_REVERSE
                    if (cost_via_k > inf)
                        cost_via_k = inf;
                    if (Routers_pre[i].dt[j][k] != cost_via_k)
                    {
                        Routers[i].dt[j][k] = cost_via_k;
                        ++count;
                        if (Routers[i].neighbours[k] && (i!=j))
                        {
                            display1(time, Routers[i].get_id(), Routers[j].get_id(), Routers[k].get_id(), cost_via_k);
                            printed = true;
                        }
                    }
                }
            if (printed)
                printf("\n");
        }



        for (int i = 0; i < num_nodes; i++)
            Routers[i].calc();

        print_all();

    } while (count != 0);
}

// ---------------------------------

bool read_config(char* filename)
{
    FILE *config_file;                          // configuration file

    config_file = fopen(filename, "r");
    if (config_file == NULL)                    // error handling
    {
        fprintf(stderr, "Error: Unable to open %s\n", filename);
        return false;
    }

    int cost;
    time = 0;

    // Read in data

    fscanf(config_file, "%d", &num_nodes);

    CRouter::count = num_nodes;

    printf("\n#START  \n");
    // Extracting Router ID
    for (int r = 0; r < num_nodes; ++r)
        if (!feof(config_file))
        {
            fgetc(config_file);
            char c = fgetc(config_file);
            Routers[r].init(c, r);
        }
        else
        {
            fprintf(stderr, "Error: incorrect in data.\n");
            return 0;
        }


    int num_links = 0;
    // Extracting Link Info
    if (!feof(config_file))
    {
        fscanf(config_file, "%d", &num_links);
    }
    else
    {
        fprintf(stderr, "Error: incorrect in data.\n");
        return 0;
    }

    for (int l = 0; l < num_links; ++l)
    {
        if (feof(config_file))
        {
            fprintf(stderr, "Error: incorrect in data.\n");
            return 0;
        }
        char s, d;                              // Source, Destination
        fscanf(config_file, "\n%c %c %d", &s, &d, &cost);
        //printf("\nsource: %c destination: %c cost: %i \n",s,d,cost);

        int si = get_index(s);
        int di = get_index(d);

        Routers[si].setCost(di, cost);
        Routers[di].setCost(si, cost);

        // displaying 2 way link info        
        display1(time, s, d, d, cost);
        display1(time, d, s, s, cost);
    }

    fclose(config_file);

    return true;
}

// ---------------------------------

bool read_ch_config(char* filename)
{
    FILE *changConfig_file;                     // configuration change file
    changConfig_file = fopen(filename, "r");
    if (changConfig_file == NULL)               // error handling
    {
        fprintf(stderr, "Error: Unable to open %s\n", filename);
        return false;
    }

    int cost;
    time = 0;
    int c_link;
    fscanf(changConfig_file, "%d", &c_link);

    for (int l = 0; l < c_link; l++)            // Extracting link change infor from change config file
    {
        if (feof(changConfig_file))
        {
            fprintf(stderr, "Error: incorrect in data.\n");
            return false;
        }

        char s, d;                              // Source, Destination
        fscanf(changConfig_file, "\n%c %c %d", &s, &d, &cost);

        int si = get_index(s);
        int di = get_index(d);

        Routers[si].setCost(di, cost);
        Routers[di].setCost(si, cost);

        // Display change in link
        printf("\n");
        display1(time, s, d, d, cost);
        display1(time, d, s, s, cost);
    }
    fclose(changConfig_file);
    return true;
}

// ---------------------------------

int main(int argc, char **argv)
{
#ifdef POISON_REVERSE
    printf("\nDistance Vector algorithm with Poisoned Reverse\n");
#else
    printf("\nDistance Vector algorithm\n");
#endif // POISON_REVERSE

    if (argc < 3)
    {
        fprintf(stderr, "Error: Not enough command line input arguments.\n");
        return 0;
    }

    if (!read_config(argv[1]))
        return 0;

    for (int i = 0; i < num_nodes; i++)         // init tables
        Routers[i].reset();
    for (int i = 0; i < num_nodes; i++)
        Routers[i].calc();
    print_all();

    printf("\n");

    update_table();                             // Updating the table

    printf("\n\n#INITIAL  \n");

    display_all();

    // Checking for link change info
    printf("\n\n#UPDATE \n");

    if (!read_ch_config(argv[2]))
        return 0;

    printf("\n");

    for (int i = 0; i < num_nodes; i++)         // init tables
        Routers[i].reset();
    for (int i = 0; i < num_nodes; i++)
        Routers[i].calc();

    print_all();

    update_table();                             // Updating the table

    // Displaying final route
    printf("\n\n#FINAL  \n");
    display_all();

    printf("\n\n");

    return 0;
}




