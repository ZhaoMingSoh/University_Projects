run:
	all ${ARGS}

make run ARGS="i.txt o.txt"

all: DistanceVector.o PoisonedReverse.o
	g++ DistanceVector.o -o  DS 
	g++ PoisonedReverse.o -o PS

DistanceVector.o: DistanceVector.cpp
	g++ -c DistanceVector.cpp 
	
PoisonedReverse.o: PoisonedReverse.cpp
	g++ -c PoisonedReverse.cpp

clean:	
	rm -rf *o DS PS