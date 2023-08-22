README.txt

Group Info
1. Heath Rusby, a1708147, a1708147@student.adelaide.edu.au
2. Zhao Ming Soh - a1751699 - a1751699@student.adelaide.edu.au


Solutions can be found within the included PDF document.

Each program is applicable to the following assignment exercise:


Exercise 3 source files are located in its own folder within the included ZIP.Outputs at each iteration of the rank calculation can be found in the subsequent rXX folders in ascending order.
These outputs are calculated using the web-Google.txt input file found at http://snap.stanford.edu/data/web-Google.html.

PLEASE NOTE: 
Node Count is hard coded into the program so if you wish to run tests on different inputs you will need to manual change this value to the number of nodes in the input file. (see line 31 of PageRank1.java)
I had issues exporting to psudo distributed mode so I performed all testing in standalone mode. The psudo distributed program runs for me but I have not tested it at length. If any problems are encountered the program will run pjsut fine in standalone
 
Running instructions:

	hadoop jar path/to/file.jar inputFile_path output_path

Be sure to add any input files to HDFS first with:

	hadoop fs -put inputFile_path





