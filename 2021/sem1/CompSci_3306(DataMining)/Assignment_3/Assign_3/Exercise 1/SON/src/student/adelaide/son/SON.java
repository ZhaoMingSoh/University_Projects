package student.adelaide.son;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;

import student.adelaide.son.SON;
import student.adelaide.son.SON.Job1Map;
import student.adelaide.son.SON.Job1Reduce;
import student.adelaide.son.SON.Job2Map;
import student.adelaide.son.SON.Job2Reduce;
import student.adelaide.son.Apriori;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Mapper.Context;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class SON extends Configured implements Tool {

	private static Double supThresh;
	private static int noOfTotalTransa;
	private int noOfSplitFiles;
	
	@Override
	public int run(String[] args) throws Exception {
		
		supThresh = Double.parseDouble(args[2]);
		String inputFileName = args[0];
		String outputFolderName = args[1];
		Path outputPath = new Path(outputFolderName);
        Path inputPath = new Path("splits/register.txt");
        
        FileSystem fs = FileSystem.get(new Configuration());
        if (fs.exists(outputPath))
            fs.delete(outputPath, true);
        
        int[]arr = splitFile(inputFileName);
        noOfTotalTransa = arr[0];
        noOfSplitFiles = arr[1];
        
        //Job1
        Job job1 = new Job(getConf(), "Job1");
        job1.setJarByClass(SON.class);
      
        FileInputFormat.addInputPath(job1, inputPath);
        job1.setInputFormatClass(TextInputFormat.class);
        job1.setMapOutputKeyClass(Text.class);
        job1.setMapOutputValueClass(IntWritable.class);
        job1.setMapperClass(Job1Map.class);
      
        FileOutputFormat.setOutputPath(job1, new Path(outputFolderName +"/Reducer1Output"));
        job1.setOutputFormatClass(TextOutputFormat.class);
        job1.setOutputKeyClass(Text.class);
        job1.setOutputValueClass(Text.class);
        job1.setReducerClass(Job1Reduce.class);
             
        if (!job1.waitForCompletion(true)) {
        	System.exit(1);
        }
        
        inputPath = new Path(outputFolderName+"/Reducer1Output");
    	outputPath = new Path(outputFolderName+"/Reducer2Output");
        
        //job2
    	Job job2 = new Job(getConf(), "Job2");
        job2.setJarByClass(SON.class);
        
        FileInputFormat.addInputPath(job2, inputPath);
        job2.setInputFormatClass(TextInputFormat.class);
        job2.setMapOutputKeyClass(Text.class);
        job2.setMapOutputValueClass(IntWritable.class);
        job2.setMapperClass(Job2Map.class);
        
        FileOutputFormat.setOutputPath(job2, outputPath);
        job2.setOutputFormatClass(TextOutputFormat.class);
        job2.setOutputKeyClass(Text.class);
        job2.setOutputValueClass(Text.class);
        job2.setReducerClass(Job2Reduce.class);
               
        if (!job2.waitForCompletion(true)) {
        	System.exit(1);
        }
        
        
		return 0;
	}
	
	public static void main(String[] args) throws Exception {
		System.out.println(Arrays.toString(args));
        int res = ToolRunner.run(new Configuration(), new SON(), args);
        
        System.exit(res);

	}
	
	public static class Job1Map extends Mapper<LongWritable, Text, Text, IntWritable> {
	       
        @Override
        public void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException {
        	
        	String fileName = value.toString();
        	System.out.println(fileName);
        	Apriori ap;
			try {
				ap = new Apriori(fileName, supThresh);
				List<String> candidates = ap.startPasses();
				
				for( String itemset: candidates){
	        		String[] split = itemset.split(":");
	        		context.write(new Text(split[0]), new IntWritable(Integer.parseInt(split[1].trim())));
	        		
				}
	        	
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
        	
        	
			
        }
    }
	 
	public static class Job1Reduce extends Reducer<Text, IntWritable, Text, IntWritable> {
		
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
        throws IOException, InterruptedException {
			int sum = 0;
			
			for (IntWritable val: values)
			{
				sum+=val.get();
			}
			Text text = new Text(key.toString() + ":");
			context.write(text, new IntWritable(sum));
        }
    }
	
	public static class Job2Map extends Mapper<LongWritable, Text, Text, IntWritable> {
	       
        @Override
        public void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException {
        	
        	String[] frequentItemset = value.toString().split(":");
        	context.write(new Text(frequentItemset[0]),new IntWritable(Integer.parseInt(frequentItemset[1].trim())));
        	
        }
    }
	 
	public static class Job2Reduce extends Reducer<Text, IntWritable, Text, Text> {
		
		@Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
        throws IOException, InterruptedException {
            
			int sum = 0;
			
			for(IntWritable freq: values) {
				sum+=freq.get();
			}
        	
        	if(sum>=supThresh*noOfTotalTransa){
        		context.write(key, new Text(" (" + Integer.toString(sum) + ")"));
        	}
        	
        }
    }
	
	private int[] splitFile(String inputPath) throws IOException {

		File inputFile = new File(inputPath);
		
		int noOfBaskets = 0;
		int support = 0;
		int splitFileNumber = 1;
		
		File file = new File("splits");
		if(!file.exists()){
			file.mkdir();
		}
		
		int linesWritten = 0;
		String line;
		int sizeInMb = (int) Math.ceil(((double) inputFile.length() / (1024 * 1024)));
		FileReader in = new FileReader(inputFile);
		BufferedReader inputReader = new BufferedReader(in);
		BufferedWriter outputWriter = null;
		
		int fileSize = 0;

		File fileNameRegister = new File("splits/register.txt");
		BufferedWriter registerWriter = new BufferedWriter(new FileWriter(fileNameRegister));
		while ((line = inputReader.readLine()) != null) {
			noOfBaskets++;
			fileSize = fileSize + line.length();
			if (linesWritten == 0) {
				File newSplitFile = new File("splits/input" + splitFileNumber+".txt");
				registerWriter.write("splits/input" + splitFileNumber++ + ".txt\n");
				outputWriter = new BufferedWriter(new FileWriter(newSplitFile));
			}

			outputWriter.write(line + "\n");
			linesWritten++;
			if ((int) (((double) fileSize) / (1024 * 1024)) >= 4) {
				linesWritten = 0;
				outputWriter.close();
				fileSize = 0;
			}
		}
		outputWriter.close();
		registerWriter.close();
		inputReader.close();
		
		
		int[] arr = {noOfBaskets, splitFileNumber-1};
		return arr;
	}

}
