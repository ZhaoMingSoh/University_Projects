#ifndef ROUTER_H
#define ROUTER_H

#include "DistanceVector.h"

class CRouter
{
public:
    CRouter();
    unsigned int dt[max_size][max_size];    // (shortest) Distance table [dest][via]
    bool neighbours[max_size];
    unsigned int ndt[max_size];             // (real) Distance to neighbours table [dest]

    void init(char _id, int _index);
    char get_id()       { return id; }
    int  get_index()    { return index; }
    void setCost(int a, unsigned int cost) { neighbours[a] = true; ndt[a] = cost; }
    void reset();

    static int count;                       // number of routers/nodes in the topology


    int getRout(int dst) { return best_rout[dst]; }
    int* getAllRout() { return best_rout; }
    int getCost(int dst) { return best_rout[dst] >= 0 ? dt[dst][best_rout[dst]] : inf; }

    void calc();

private:
    int     best_rout[max_size];
    char    id;
    int     index;
};




#endif // ROUTER_H
