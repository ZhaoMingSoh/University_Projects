-raw output files can be located in the "outputs" folder
-all source & program files for exercise 1 can be found in "simpleRandomised" and "SON" folders


------------------Simple Randomized Algorithm---------------------------
JAVA files can be found in "/SimpleRandomized/src/student/adelaide/simplerandomized"

To use JAR file.
	In SimpleRandomized folder:
		java -jar SimpleRandomised.jar inputs/filename.txt outputFolderName SampleSize SupportThreshold
		eg. java -jar SimpleRandomised.jar inputs/chess.txt output 0.05 0.9

		Note: 	The above example will create or overwrite the file 
			output/FrequentItemsets_sampleSize0.05.txt to store results.
			It will also create or overwrite output/SelectedSamples.txt 
			with the random sample generated from the dataset that was 
			used in the A-Priori algorithm



------------------SON Algorithm---------------------------
JAVA files can be found in "/SON/src/student/adelaide/son"

Unfortunetly my current eclipse environment is having issues when exported jars are not working with mapreduce.
I have included the jar and its intended use but was getting an library related error that I couldnt fix. 
If this error persists on your system then the java files can be run in eclipse with the same argument format as below.

To use JAR file. (not working on my system)
	In SON folder:
		java -jar SON.jar inputs/filename.txt outputFolderName SupportThreshold
		eg. java -jar SON.jar inputs/chess.txt output 0.9

		Note:	The above example will create/overwride a folder called 
			"splits" which will store each chunk of the input dataset.
			The list of frequent datasets and their frequencies can be 
			found in outputSON/Reducer2Output/part-r-00000.txt (frequency 
			is dentoted by bracketed number after the itemset)
