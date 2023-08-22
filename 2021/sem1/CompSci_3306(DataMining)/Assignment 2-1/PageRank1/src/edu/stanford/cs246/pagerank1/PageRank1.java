package edu.stanford.cs246.pagerank1;

import java.io.IOException;
import java.util.*;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Mapper.Context;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import edu.stanford.cs246.pagerank1.PageRank1;



public class PageRank1 extends Configured implements Tool {
	
	private static Integer nodeCount = 875713; //provided in file
	
	public static void main(String[] args) throws Exception {
		System.out.println(Arrays.toString(args));
        int res = ToolRunner.run(new Configuration(), new PageRank1(), args);
        
        System.exit(res);

	}
	
	public int run(String[] args) throws Exception {
		 System.out.println(Arrays.toString(args));
        @SuppressWarnings("deprecation")
        
        Path outputPath = new Path(args[1]);
        Path inputPath = new Path(args[0]);
        FileSystem fs = FileSystem.get(new Configuration());
        if (fs.exists(outputPath))
            fs.delete(outputPath, true);
        
        //Job1 - Initialization of input
		Job job1 = new Job(getConf(), "Job1");
        job1.setJarByClass(PageRank1.class);
        
        FileInputFormat.addInputPath(job1, inputPath);
        job1.setInputFormatClass(TextInputFormat.class);
        job1.setMapOutputKeyClass(Text.class);
        job1.setMapOutputValueClass(Text.class);
        job1.setMapperClass(Job1Map.class);
        
        FileOutputFormat.setOutputPath(job1, new Path(args[1]+"/r0"));
        job1.setOutputFormatClass(TextOutputFormat.class);
        job1.setOutputKeyClass(Text.class);
        job1.setOutputValueClass(Text.class);
        job1.setReducerClass(Job1Reduce.class);
               
        if (!job1.waitForCompletion(true)) {
        	System.exit(1);
        }
        
        //PageRank calculation
        for (Integer iteration = 0; iteration < 50; iteration++) {
        	System.out.println("Running iteration:" + Integer.toString(iteration));
        	 System.out.println("input: r"+Integer.toString(iteration)+", output: " + Integer.toString(iteration+1));
        	inputPath = new Path(args[1]+"/r"+Integer.toString(iteration));
        	outputPath = new Path(args[1]+"/r"+Integer.toString(iteration+1));
        	
        	//job2
        	Job job2 = new Job(getConf(), "Job2");
            job2.setJarByClass(PageRank1.class);
            
            FileInputFormat.addInputPath(job2, inputPath);
            job2.setInputFormatClass(TextInputFormat.class);
            job2.setMapOutputKeyClass(Text.class);
            job2.setMapOutputValueClass(Text.class);
            job2.setMapperClass(Job2Map.class);
            
            FileOutputFormat.setOutputPath(job2, outputPath);
            job2.setOutputFormatClass(TextOutputFormat.class);
            job2.setOutputKeyClass(Text.class);
            job2.setOutputValueClass(Text.class);
            job2.setReducerClass(Job2Reduce.class);
                   
            if (!job2.waitForCompletion(true)) {
            	System.exit(1);
            }
        	
        }
        
        inputPath = new Path(args[1]+"/r20");
    	outputPath = new Path(args[1]+"/rfinal");
    	
    	//job3
    	Job job3 = new Job(getConf(), "Job3");
        job3.setJarByClass(PageRank1.class);
        
        FileInputFormat.addInputPath(job3, inputPath);
        job3.setInputFormatClass(TextInputFormat.class);
        job3.setMapOutputKeyClass(DoubleWritable.class);
        job3.setMapOutputValueClass(Text.class);
        job3.setMapperClass(Job3Map.class);
        
        FileOutputFormat.setOutputPath(job3, outputPath);
        job3.setOutputFormatClass(TextOutputFormat.class);
        job3.setOutputKeyClass(DoubleWritable.class);
        job3.setOutputValueClass(Text.class);
        job3.setReducerClass(Job3Reduce.class);
               
        if (!job3.waitForCompletion(true)) {
        	System.exit(1);
        }
        
        System.out.println("DONE!");   
        return 0;
	}
	
	
	public static class Job1Map extends Mapper<LongWritable, Text, Text, Text> {
       
        private String [] row;
        private Text fromNode;
        private Text toNode;
        
        @Override
        public void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException {
        	if (value.charAt(0) != '#') {
        		row = value.toString().split("\\s"); 
            	fromNode = new Text(row[0]);
            	if (row.length == 1)
            	{
            		return;
            	}
            	
            	toNode = new Text(row[1]);
            	context.write(fromNode, toNode);
        	}
        	
        }
    }
	 
	public static class Job1Reduce extends Reducer<Text, Text, Text, Text> {
		
		
		@Override
        public void reduce(Text key, Iterable<Text> values, Context context)
        throws IOException, InterruptedException {
            
			Boolean firstFlag = true;
			
        	String links = Double.toString(0.85/nodeCount) + "\t";
        	
        	for (Text toNode: values) {
        		
        		if (!firstFlag) {
        			links += ",";
        		}
        		links+=toNode.toString();
        		firstFlag = false;
        	}
        	
        	
        	context.write(key, new Text(links));        	
        	
        }
    }
	
	public static class Job2Map extends Mapper<LongWritable, Text, Text, Text> {
	       
        private String [] row;
        private String fromNode;
        private String pageRank;
        private String links;
        
        @Override
        public void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException {
        	
        	row = value.toString().split("\\s");
        	fromNode = row[0];
        	pageRank = row[1];
        	if (row.length>2)
        		links = row[2];
        	else
        		links = "";
        		
        	String[] linksSeperated = links.split(",");
        	for(String toNode: linksSeperated) {
        		context.write(new Text(toNode), new Text(pageRank +"\t" + linksSeperated.length));
        	}
        	
        	if(links != "")
        	{
        		context.write(new Text(fromNode), new Text("@" + links));
        	}
        	
        	
        }
    }
	
	public static class Job2Reduce extends Reducer<Text, Text, Text, Text> {
		
		private String[] row;
		private String links;
		private Double pageRank;
		private Double newRank;
		private Integer linkCount;
		private Double sumLinkRanks;
		@Override
        public void reduce(Text key, Iterable<Text> values, Context context)
        throws IOException, InterruptedException {
        
			links = "";
			sumLinkRanks = 0.0;
			
        	for (Text value: values) {
        		
        		String stringValue = value.toString();
        		if (stringValue.charAt(0)=='@') {
        			links += stringValue.substring(1);
        			
        		}
        		else
        		{
        			row = stringValue.split("\\t");
        			pageRank = Double.parseDouble(row[0]);
        			linkCount = Integer.parseInt(row[1]);
        			sumLinkRanks += (pageRank/linkCount);
        	
        		}
        	}
        
        	newRank = 0.85 * sumLinkRanks + (1-0.85)/nodeCount; // 15% chance of surfer wont follow outlink and start at random page
        	context.write(key, new Text(newRank + "\t" + links));        	
        	
        }
    }
	
	public static class Job3Map extends Mapper<LongWritable, Text, DoubleWritable, Text> {
	       
        private Text fromNode;
        private Double pageRank;
        private String[] row;
        
        @Override
        public void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException {
        	
        	row = value.toString().split("\\s");
        	fromNode = new Text(row[0]);
        	pageRank = Double.parseDouble(row[1]);
        	
        	context.write(new DoubleWritable(pageRank),fromNode);
        	
        }
    }
	
	public static class Job3Reduce extends Reducer<DoubleWritable, Text, DoubleWritable, Text> {
		
		@Override
        public void reduce(DoubleWritable key, Iterable<Text> values, Context context)
        throws IOException, InterruptedException {
        
			for (Text value: values)
			{
				context.write(key, value);
			}
		}
    }
	
	
	

}//end PageRank