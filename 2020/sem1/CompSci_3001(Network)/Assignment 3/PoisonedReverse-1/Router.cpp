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

void CRouter::reset()
{
    for (int i = 0; i < max_size; ++i)
        if (neighbours[i])
            dt[i][i] = ndt[i];
}

void CRouter::calc()
{
    for (int dest = 0; dest < count; ++dest)
    {
        unsigned int best_cost = inf;

        for (int via = 0; via < count; ++via)
            if ((best_cost > dt[dest][via]) && (neighbours[via]||(index == dest)))
            {
                best_rout[dest] = via;
                best_cost = dt[dest][via];
            }

        dt[dest][index] = best_cost;
    }
}

