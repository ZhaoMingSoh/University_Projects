package student.adelaide.simplerandomized;

import java.io.*;
import java.util.*;
import java.io.*;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

import student.adelaide.simplerandomized.Apriori;

public class SimpleRandomized {


	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		Double supThresh = Double.parseDouble(args[3]);
		Double sampleSize = Double.parseDouble(args[2]); 
		String outputsFolder = args[1];
        String inputFileName = args[0];
       
        
        long start = System.currentTimeMillis();
        
        try{
        	File sampleFile = new File(outputsFolder + "/SelectedSamples.txt");
        	sampleFile.getParentFile().mkdirs();
        	sampleFile.createNewFile();
        
	        BufferedReader data_in = new BufferedReader(new FileReader(inputFileName));
	        FileWriter fw = new FileWriter(outputsFolder + "/SelectedSamples.txt");
	        Random rand = new Random();
	        Long sampleCount = (long) 0;
	        Long totalCount = (long) 0;
	        
	        //loop through input file and select rows based on inputed percentage (sampleSize)
	        while(data_in.ready()) 
			{
				String row = data_in.readLine();
				totalCount++;
				if((row.matches("//s*"))||(rand.nextDouble()>sampleSize)) continue; //only take percentage of transactions. skip empty rows
				fw.write(row +"\n");
				sampleCount++;
			}
			data_in.close();
			fw.close();
			System.out.println("Sample size: " + sampleSize + " (" + sampleCount + " of " + totalCount + ")");
        } catch (IOException e) {
        	System.out.println("error occured with random sample generation");
        	System.exit(1);
        }
        
        
        
        FileSystem fs = FileSystem.get(new Configuration());
        if (fs.exists(new Path(outputsFolder + "/FrequentItemsets_sampleSize"+sampleSize+".txt")))
            fs.delete(new Path(outputsFolder + "/FrequentItemsets_sampleSize"+sampleSize+".txt"), true);
        
        //Perform Apriori algorithm on selected samples with 1% support threshold
		Apriori ap = new Apriori(outputsFolder + "/SelectedSamples.txt",outputsFolder + "/FrequentItemsets_sampleSize"+sampleSize+".txt", supThresh);
		ap.startPasses();
		
		long end = System.currentTimeMillis();
		float runtime = (end-start)/(float)1000;
		System.out.printf("Runtime: %.2f seconds%n",runtime);
	}

}
