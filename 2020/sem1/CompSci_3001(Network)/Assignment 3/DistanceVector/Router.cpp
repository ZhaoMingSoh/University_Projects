#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "Router.h"

int CRouter::count = 0;

CRouter::CRouter()
{
    for (int i = 0; i < max_size; ++i)
    {
        for (int j = 0; j < max_size; ++j)
            dt[i][j] = inf;
        best_rout[i] = -1;
        neighbours[i] = false;
    }

    id = '?';
    index = -1;
}

void CRouter::init(char _id, int _index)
{
    id = _id;
    index = _index;
    dt[index][index] = 0;
}

// Initialise the dt[dest][via] for neighbors based on values in ndt
// Set the cost of the Router -> Dest via Neighbor 
void CRouter::reset()
{
    for (int i = 0; i < max_size; ++i)
        if (neighbours[i])
            dt[i][i] = ndt[i];
}

// Calculates the best cost with the best route for the [router -> dest via index] based on the lastest dt[dest][via] state
void CRouter::calc()
{
    printf("\n");
    for (int dest = 0; dest < count; ++dest)
    {
        unsigned int best_cost = inf;
        // printf("Dest[%d] - best_cost : %d", dest, best_cost);
        for (int via = 0; via < count; ++via)
            // The dest the router goes to has to be from a connected neighbor, the dest cannot be itself
            if ((best_cost > dt[dest][via]) && (neighbours[via]||(index == dest)))
            {
                best_rout[dest] = via; // Find the new best route of Router -> Dest via (neigh out of [0 to N-1])
                best_cost = dt[dest][via];
                // printf("Via[%d] - best_cost : %d", via, best_cost);
            }
        // printf("\n");
        dt[dest][index] = best_cost; // Find the new best cost of Router -> Dest via itself
    }
}

