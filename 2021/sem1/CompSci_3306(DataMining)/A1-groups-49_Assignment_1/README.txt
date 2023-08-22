README.txt

A1-groups 49

a1745714 - Charles Hibbert
A1751699 - Zhao Ming Soh

<-------------------------------------------------------------------------------------------------------------------------------------------------------------------------->

Exercise 2 - 

<File Location> -> Assign_1/Source_Files/Exercise_2 (This is a java project)

- - - - - - - - - - - - - - - - - - - -- - - - - - - - - -- - - - - - -- -- - - - -
(Since what I provide is the entire Exercise_2 project directory, all the existing files are in :) 
1. Standalone Mode existing Output Files :
	a. Assign_1/Source_Files/Exercise_2/Output_Files/output 

2. Pseudo-Distributed Mode existing Output Files :
	b. Assign_1/Source_Files/Exercise_2/Pseudo_Distributed/output_exercise_2

3. The Hadoop HDFS log files obtained from the localhost :
	c. Assign_1/Source_Files/Exercise_2/Pseudo_Distributed/output_exercise_2/LogFiles_From_Hadoop_LocalHost
- - - - - - - - - - - - - - - - - - - -- - - - - - - - - -- - - - - - -- -- - - - -

To run in the Standalone Mode :

1. Open Eclipse 
2. Right-click in the "Package Explorer" 
3. Click on the import option and in the select directory, browse the path to the Exercise_2 project and click finish
4. Right-click on the Exercise_2 project directory and select "Run Configurations as ....." 
5. In the "Main" interface, key in the Project name "Exercise_2" in the "Project" input area, and key in the Main class name "edu.stanford.cs246.wordcount".
6. In the "Argument" interface, key in "pg100.txt output" 
7. Click Apply and Run

- - - - - - - - - - - - - - - - - - - -- - - - - - - - - -- - - - - - -- -- - - - -

To run in the Pseudo-Distributed Mode :

<File Location> --> Assign_1/Source_Files/Exercise_2/Pseudo_Distributed 

1. Open your terminal and go to the Pseudo_Distributed directory
2. Key in the following into your terminal :
	a. Hadoop jar WordCount.jar ./pg100.txt ./ex2_pseudo_distributed_output 
	b. (To obtain the file -> (ex2_pseudo_distributed_output) from the HDFS) 
		1. Key in "Hadoop fs -get ./ex2_pseudo_distributed_output"

<-------------------------------------------------------------------------------------------------------------------------------------------------------------------------->

<File Location> -> Assign_1/Source_Files/Exercise_3 

To run Exercise 3 -

1. Download and install VirtualBox
2. Download and install Cloudera Quickstart VM
3. Start the Cloudera Vm
4. Open Eclispe
5. Duplicate the training node in the Package Explorer
6. Make project name MF
5. Create a new package called MFp
6. Create a new class in this package called mutualFriendsC
a) In the pop-up dialog, enter WordCount as the Name. See Figure 21.
b) In the Superclass field, enter Configured and click the Browse button. From the popup window select Configured − org.apache.hadoop.conf and click the OK button.
c) In the Interfaces section, click the Add button. From the pop-up window select Tool −
org.apache.hadoop.util and click the OK button. 
d) Check the boxes for public static void main(String args[]) and Inherited abstract methods and click the Finish button.
7. Copy the contents of the given'mutualFriendsC.java' file, into this class.
8. Place the given input file into the ~/workspace/MF directory, and name the file 'friends.txt'.

(To run in standalone mode:)

9. Right click on the project select Run -> Run Configurations
10. In the pop-up dialog, select the Java Application node and click the New launch configuration button in the upper left corner.
11. Enter a name in the Name field and MF in the Main class field.
12. Switch to the Arguments tab and put friends.txt output in the Program arguments
13. Right-click on the project and select Run As → Java Application.
14. In the pop-up dialog select MF - MFp from the selection list and click OK.
15. Fund th eresults in ~worksplace/MF/output directory

(To run in pseudo-distributed mode:)

9. Right-click on the project and select Export.
10. Expand the Java node and select JAR file. Click Next.
11. Enter /home/cloudera/MF.jar in the JAR file field and click Finish.
12. Open a terminal in your VM and traverse to the folder /home/cloudera and run the
following commands:
hadoop fs -put workspace/MF/friends.txt
hadoop jar MF.jar MFp friends.txt output
13. Run the command: hadoop fs -ls output
14. Run the command: hadoop fs -cat output/part\* | head
You should see the same output as when you ran the job in standalone mode.
15. To view the job’s logs, open the browser in the VM and point it to http://localhost: 8088
16. Click on the link for the completed job. 
17. Click the link for the map tasks.
18. Click the link for the first attempt.
19. Click the link for the full logs.

<-------------------------------------------------------------------------------------------------------------------------------------------------------------------------->

Exercise 4 - 

<File Location> Assign_1/Source_Files/Exercise_4 (This is a project file) 

- - - - - - - - - - - - - - - - - - - -- - - - - - - - - -- - - - - - -- -- - - - -
(Since what I provide is the entire Exercise_4 project directory, all the existing files are in :) 
1. Part_1 Output files :
	a. Assign_1/Source_Files/Exercise_2/Output_Files 
		a) Part_1_100_txt_output
		b) Part_1_3399_txt_output

2. Part_3 Output files :
	b. Assign_1/Source_Files/Exercise_2/Output_Files 
		a) Part_3_100_txt_output
		b) Part_3_3399_txt_output

3. (Both the processed input files are already stored in the following location :)
	a. lowercase files : 
		a) Assign_1/Source_Files/Exercise_4/Part_1_Input_Files
	b. No punctuation and lowercase files : 
		b) Assign_1/Source_Files/Exercise_4/Part_3_Input_Files

- - - - - - - - - - - - - - - - - - - -- - - - - - - - - -- - - - - - -- -- - - - -
(This is only here for evidence purpose)

<The python code that is used to transform the pg100.txt and 3399.txt files for each part : Assign_1/Source_Files/Parse_inputFiles_for_Exercise_4
(This will produce 4 input files :
		a. lowercase files : 
			1. pg100_lower.txt
			2. pg3399_lower.txt
		b. No punctuation and lowercase files :
			1. pg100_no_punct.txt
			2. 3399_no_punct.txt

- - - - - - - - - - - - - - - - - - - -- - - - - - - - - -- - - - - - -- -- - - - -
- - - - - - - - - - - - - - - - - - - -- - - - - - - - - -- - - - - - -- -- - - - -

(Since the I zipped the entire Exercise_4 directory/project, you can simply run it by following the steps below :)

1. Part 1 - (pg100.txt Case) 
	a. Open Eclipse 
	b. Right-click in the "Package Explorer" 
 	c. Click on the import option and in the select directory, browse the path to the Exercise_4 project and click finish
 	d. Right-click on the Exercise_4 project directory and select "Run Configurations as ....." 
	e. In the "Main" interface, key in the Project name "Exercise_4" in the "Project" input area, and key in the Main class name "exercise_4.exercise_4_Part_1".
 	f. In the "Argument" interface, key in "/home/cloudera/workspace/Exercise_4/Part_1_Input_Files/pg100_lower.txt Part_1_100_txt_output" 
 	g. Click Apply and Run
	
	(3399.txt case) -
	a. Open Eclipse 
	b. Right-click in the "Package Explorer" 
 	c. Click on the import option and in the select directory, browse the path to the Exercise_4 project and click finish
 	d. Right-click on the Exercise_4 project directory and select "Run Configurations as ....." 
	e. In the "Main" interface, key in the Project name "Exercise_4" in the "Project" input area, and key in the Main class name "exercise_4.exercise_4_Part_1".
 	f. In the "Argument" interface, key in "/home/cloudera/workspace/Exercise_4/Part_1_Input_Files/pg3399_lower.txt Part_1_3399_txt_output" 
 	g. Click Apply and Run

- - - - - - - - - - - - - - - - - - - -- - - - - - - - - -- - - - - - -- -- - - - -

2. Part 3 - (pg100.txt Case)
	a. Open Eclipse 
	b. Right-click in the "Package Explorer" 
 	c. Click on the import option and in the select directory, browse the path to the Exercise_4 project and click finish
 	d. Right-click on the Exercise_4 project directory and select "Run Configurations as ....." 
	e. In the "Main" interface, key in the Project name "Exercise_4" in the "Project" input area, and key in the Main class name "exercise_4.exercise_4_Part_3".
 	f. In the "Argument" interface, key in "/home/cloudera/workspace/Exercise_4/Part_1_Input_Files/pg100_no_punct.txt Part_3_100_txt_output" 
 	g. Click Apply and Run
	
	(3399.txt case) -
	a. Open Eclipse 
	b. Right-click in the "Package Explorer" 
 	c. Click on the import option and in the select directory, browse the path to the Exercise_4 project and click finish
 	d. Right-click on the Exercise_4 project directory and select "Run Configurations as ....." 
	e. In the "Main" interface, key in the Project name "Exercise_4" in the "Project" input area, and key in the Main class name "exercise_4.exercise_4_Part_3".
 	f. In the "Argument" interface, key in "/home/cloudera/workspace/Exercise_4/Part_1_Input_Files/3399_no_punct.txt Part_3_3399_txt_output" 
 	g. Click Apply and Run
	





