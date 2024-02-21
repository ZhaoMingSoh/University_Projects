# Key Points about this algorithm

Let's take the Input1.txt as a example :
After the readConfig() in DistanceVector.cpp -
**dt in each router :**
Router[0] : X  
0 inf inf  
inf inf inf  
inf inf inf  
Router[1] : Y
inf inf inf  
inf 0 inf  
inf inf inf  
Router[2] : Z
inf inf inf  
inf inf inf  
inf inf 0

**neighbor[] & its ndt[] in each router:**
Router[0] : X
neighbour[F T T]
ndt[0 2 7]

Router[1] : Y
neighbour[T F T]
ndt[2 0 1]

Router[2] : Z
neighbour[T T F]
ndt[7 1 0]

### 1) CRouter::reset() in Router.cpp

This function will initialise all of the router's connected neighbours cost to each of their dt

**dt in each router : Visible along the diagonal of the dt**
Router[0] : X  
0 inf inf  
inf 2 inf  
inf inf 7  
Router[1] : Y
2 inf inf  
inf 0 inf  
inf inf 1  
Router[2] : Z
7 inf inf  
inf 1 inf  
inf inf 0

### 2) CRouter::calc() in Router.cpp

This function will find the **best cost** of the **router to every destination** along with the **best route** to get there based on the **latest state** of the dts.

The key here lies in the conditionals of the function :

- Find the smallest cost from routers to the destination via intermediate nodes [X,Y,Z], which represents all possible routers & the intermediate nodes must be connected to the routers.
- _Special Case_ :
  - If the index === destination : we also need to take into account the smallest cost of going from routers to themselves.

When the smallest cost is found and the intermediate node through which the cost is established is also connected to the router, place the smallest cost to the **router[dest][index]**.

**dt in each router :**
Router[0] : X  
0 inf inf  
2 2 inf  
7 inf 7  
best_rout[0 1 2] : each index represent the destination through which the best route can be found

Router[1] : Y
2 2 inf  
inf 0 inf  
inf 1 1  
best_rout[0 1 2]

Router[2] : Z
7 inf 7  
inf 1 1  
inf inf 0
best_rout[0 1 2]

### 3) update_table() in DistanceVector.cpp

(All of the same routers)
s = i = source of router
d = j = destination router
intermediate node = k = intermediate router

This is function here finds any cost (not necessarily least cost) from s->d via all possible [k]s, once a different value is found by the bellman ford equation, "r[i].dt[j][k] = r[i].ndt[k] + r[k].getCost(j)" for that specific i->j via that k, update the router's dt (again) for that specific i-j via that k.

**dt in each router before the calc() in this function :**
Router[0]
0 4 14
2 2 8
7 3 7
Router[1]
2 2 8
4 0 2
9 1 1
Router[2]
7 3 7
9 1 1
14 2 0

**dt in each router after the calc() in this function :**
Router[0]
0 4 10
2 2 8
3 3 7
best_rout[0 1 1]

Router[1]
2 2 4
4 0 2
5 1 1
best_rout[0 1 2]

Router[2]
7 3 3
9 1 1
10 2 0
best_rout[1 1 2]

The update will keep going until there's no changes left in the dt of every routers meaning count becomes 0 and the forever loop breaks (convergence of the algo).

### What happens after the read_ch_config() ?

1. No Count-To-Infinity Changes :
   Proceed as normal.

2. Count-To-Infinity is introduced where the edges cost changed is too big :

   - There will be an infinite bounce between a couple of routers in the least cost calculation.
   - Based on the changedInput1.txt :
     X Y 2 increases to X Y 60 (bad news travel slow)

     **dt of each router after reset() & calc()**
     Router[0] : X
     0 4 10
     8 60 8
     3 3 7
     best_rout[0 2 1]

     Router[1] : Y
     60 4 4
     4 0 2
     5 1 1
     best_rout[2 1 2]

     Router[2] : Z
     7 3 3
     9 1 1
     10 2 0
     best_rout[1 1 2]

     **update_table()**
     After the first update :
     t=1 distance from Z to X via Y is 5
     **dt table after the calc()**
     Router[0] : X
     0 64 10
     8 60 8
     7 61 7
     best_rout[0 2 2]

     Router[1] : Y
     60 4 4
     68 0 2
     63 1 1
     best_rout[2 1 2]

     Router[2] : Z
     7 5 5
     15 1 1
     10 2 0
     best_rout[1 1 2]

   Look at textbook for further explanation : [text](<../Uni Courses/2020_Adelaide_Uni/2020_Sem1/CompSci_3001(Network)/TextBooks/James F. Kurose, Keith W. Ross - Computer Networking - A Top-down Approach-Pearson (2017).pdf>)

   t=2 distance from Y to X via Z is 6
   t=3 distance from Z to X via Y is 7
   t=4 distance from Y to X via Z is 8
   **dt table after the calc()**
   After updating t=4,

   Router[0] : X
   0 66 14
   8 60 8
   7 61 7
   best_rout[0 2 2]

   Router[1] : Y
   60 8 8
   68 0 2
   67 1 1
   best_rout[2 1 2]

   Router[2] : Z
   7 7 7
   15 1 1
   14 2 0
   best_rout[0 1 2]

   t=5 distance from Z to X via Y is 9
   **dt table after the calc()**
   After updating t=5,
   Router[0]
   0 68 14
   8 60 8
   7 61 7
   best_rout[0 2 2]
   Router[1]
   60 8 8
   68 0 2
   67 1 1
   best_rout[2 1 2]
   Router[2]
   7 9 7
   15 1 1
   14 2 0
   best_rout[0 1 2]

   because of the calc() works, it will always pick Router[2][0] for Z -> X via X as the best route and best cost. Therefore, the update_table() stops executing as all the tables reached convergence which isn't supposed to happen. I guess this is a consequence of how my algo is implemented.

   Supposedly, the algo should keep going until :
   From the textbook linked above : How long will the process continue? You should convince yourself that the loop will persist for 44 iterations (message exchanges between y and z)—until z eventually computes the cost of its path via y to be greater than 50. At this point, z will (finally!) determine that its least-cost path to x is via its direct connection to x. y will then route to x via z.

   I'll think about it another time on how to simulate an infinite loop.

### The Poisoned Reverse :

**In the update_table()**
C++```
#ifdef POISON_REVERSE
if (Routers[i].neighbours[k] && (i!=j))
if (Routers_pre[k].getRout(j) == i)
cost_via_k = inf;
#endif // POISON_REVERSE

```
Initial cost from X to Y is 2.
If a link failure occurs on the link X-Y, X advertises this information to its neighbors with an infinite metric.
When Y receives this update, it recognizes that the route to X through Y is no longer valid (due to Poison Reverse), preventing the count-to-infinity problem.
```
