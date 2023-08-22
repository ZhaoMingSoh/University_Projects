package mutualFriendsP;

import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.util.Tool;

import java.io.IOException;
import java.util.*;
import java.lang.Runnable;

import javax.naming.NamingException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.mapred.jobcontrol.JobControl;           
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat; 
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;   
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.jobcontrol.ControlledJob;          
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;


public class mutualFriendsC extends Configured implements Tool {
   public static void main(String[] args) throws Exception {
      if (args.length!=2){
          System.out.println("Usage: FriendRecommendation <input dir> <output dir> \n");
          System.exit(-1);
      }
      System.out.println(Arrays.toString(args));
      int res = ToolRunner.run(new Configuration(), new mutualFriendsC(), args);
     
      System.exit(res);
   }
  
   public int run(String[] args) throws Exception {
       System.out.println(Arrays.toString(args));
       @SuppressWarnings("deprecation")
       String intermediateFileDir = "tmp";
       String intermediateFileDirFile =intermediateFileDir +"/part-r-00000";
       JobControl control = new JobControl("ChainMapReduce");
       ControlledJob step1 = new ControlledJob(jobListFriends(args[0], intermediateFileDir), null);
       ControlledJob step2 = new ControlledJob(jobRecommendFriends(intermediateFileDirFile, args[1]), Arrays.asList(step1));
       control.addJob(step1);
       control.addJob(step2);
       Thread workFlowThread =  new Thread(control, "workflowthread");
       workFlowThread.setDaemon(true);
       workFlowThread.start();  
       return 0;
   }

/* The code above is the driver for the chained MapReduce jobs. The file output path for MapReduce job 1 must match exactly with the file input path for MapReduce job 2. Another critical issue is that we need to specify the dependency in "ControlledJob step2" so that MapReduce job 2 will only start to run after the first MapReduce job completes. */



   private Job jobListFriends(String inputPath, String outputPath) throws IOException, InterruptedException, ClassNotFoundException{      
       @SuppressWarnings("deprecation")
	Job job = new Job();
       job.setJarByClass(mutualFriendsC.class);
       job.setOutputKeyClass(Text.class);
       job.setOutputValueClass(IntWritable.class);

       job.setMapperClass(Map.class);
       job.setReducerClass(Reduce.class);

       job.setInputFormatClass(KeyValueTextInputFormat.class);   // Need to change the import
       job.setOutputFormatClass(TextOutputFormat.class);

       FileInputFormat.addInputPath(job, new Path(inputPath));
       FileOutputFormat.setOutputPath(job, new Path(outputPath));

       job.waitForCompletion(true);

       return job;
   }


/* The code above setup all the configuration for MapReduce job 1. */



   private Job jobRecommendFriends(String inputPath, String outputPath) throws IOException, InterruptedException, ClassNotFoundException{     
       Job job1 = new Job();
       job1.setJarByClass(mutualFriendsC.class);
       job1.setOutputKeyClass(Text.class);
       job1.setOutputValueClass(Text.class);
      
       job1.setMapperClass(MapRecommendation.class);
       job1.setReducerClass(ReduceRecommendation.class);
      
       job1.setOutputFormatClass(TextOutputFormat.class);
       job1.setInputFormatClass(KeyValueTextInputFormat.class);

       FileInputFormat.addInputPath(job1, new Path(inputPath));
       FileOutputFormat.setOutputPath(job1, new Path(outputPath));

       job1.waitForCompletion(true);

       return job1;
      
   }


/* The code above setup all the configuration for MapReduce job 2. */
 
   public static class Map extends Mapper<Text, Text, Text, Text> {
      public final static IntWritable ZERO = new IntWritable(0);
      public final static IntWritable ONE = new IntWritable(1);

      @Override
      public void map(Text key, Text value, Context context) throws IOException, InterruptedException{
          ArrayList <String> friendList = new ArrayList<String>();

          		//takes the input and formats it in (key, value) format
          		if (!key.toString().isEmpty()){
          			for (String token: value.toString().split(",")) {
          				friendList.add(token);
          				context.write(key, new Text("r=" + token + ";m=0"));
          			}
        
          			for (int i=0; i<friendList.size();i++){
          				for (int j=0;j<friendList.size();j++){
          					if (i!=j){
          						context.write(new Text(friendList.get(i)), new Text("r=" + friendList.get(j) + ";m=1"));
          					}
          				}
          			}
          		}
      	}
   	}

/* The code above is the Mapper for the first MapReduce job. We need add a mark "zero" here if the pair <userID1, userID2> are found to be friends already which will be discared in the Reducer stage. */
 
   public static class Reduce extends Reducer<Text, Text, Text, Text> {
      public void reduce(Text key, Iterable<Text> value, Context context)throws IOException, InterruptedException {
         
    	  ArrayList<ArrayList<Integer>> mutuals = new ArrayList<ArrayList<Integer>>();
    	  int count = 0;
    	  
    	  //takes input and places in 2d array list for mapping
    	  	for(Text val: value){
    		  	String tmpStr = value.toString().substring(value.toString().indexOf(";")+1, value.toString().length());
    		  	mutuals.get(count).add(2,Integer.parseInt(value.toString().substring(0, value.toString().indexOf(";")-1)));
    			mutuals.get(count).add(1,Integer.parseInt(tmpStr.toString().substring(tmpStr.toString().indexOf("=")+1), tmpStr.toString().length()));
    		  	count++;
    	  	}


		  //adds up mutual friends, or deletes if the pair are already friends, and ouputs in (key, value) format
    	  for(int i = 0; i<count; i++){
    		  for(int j = i; j<count; j++){
    			  if(mutuals.get(i).get(0) == mutuals.get(j).get(0)){
    				  if(mutuals.get(i).get(1) == 0 || mutuals.get(j).get(1) == 0){
    					  mutuals.remove(i);
    					  mutuals.remove(j);
    				  }
    				  else{
    					  int sum = mutuals.get(i).get(1) + mutuals.get(j).get(1);
    					  mutuals.get(i).set(1, sum);
    				  }
    			  }
    		  }
    		  context.write(key, new Text("r=" +  mutuals.get(i).get(0) + ";m=" + mutuals.get(i).get(1)));
    	  }
      }  
   }
    //  public void cleanup(javax.naming.Context context) throws IOException, InterruptedException, NamingException{
    //      context.close();
    //  }

   /* The code above is the Reducer for the first MapReduce job. We need delete the pair <userID1, userID2> which are found to be friends already and marked with "Zero" in the value of the input in the Mapper stage. */


   public class MapRecommendation extends Mapper<Text, Text, Text, Text> {
       @Override
       public void map(Text key, Text value, Context context) throws IOException, InterruptedException{
           context.write(key, value);
       }
   }
   
/* The Mapper for the second MapReduce job */
  
  public static class ReduceRecommendation extends Reducer<Text, Text, Text, Text> {
      
       public void reduce (Text key, Iterable<Text> value, Context context) throws IOException, InterruptedException {

          ArrayList<friendRec> fRec = new ArrayList<friendRec>();
          int count = 0;

          //places inputs into an object arraylist
          for(Text val: value){
        	  friendRec newF  = new friendRec();
        	  String temporaryStr = value.toString().substring(value.toString().indexOf(";")+1, value.toString().length());
    		  newF.addFriend(value.toString().substring(0, value.toString().indexOf(";")-1), Integer.parseInt(temporaryStr.substring(temporaryStr.indexOf("=")+1), temporaryStr.length()));
    		  fRec.add(newF);
    		  count++;
          }

          //using compare class and sort(), orders mutual friends in order of most mutual friends to least
          compareFriends sortF = new compareFriends();
          Collections.sort(fRec, sortF);
          
          String Recommendations = "";
          
          int n;

          
          if(fRec.size()>10){
        	  n = 10;
          }
          else n = fRec.size();
          
          //ouputs at least the top 10 friend recommendations by number of mutual friends
          for(int i = 0; i<n; i++){
        	  if(n != n-1){
        		  Recommendations += fRec.get(i).getID();
        		  Recommendations += ",";
        				  
        	  }
        	  else{
        		  Recommendations += fRec.get(i).getID();
        	  }
          }
          
          context.write(key,  new Text(Recommendations));
          
       }
   }

   //friendrec class for use in second reduction
   public static class friendRec{
	   String friendRecId;
	   int friendRecNo;
	   
	   public void addFriend(String ID, int no){
		   this.friendRecId = ID;
		   this.friendRecNo = no;
	   }
	   
	   int getNo(){
		   return friendRecNo;
	   }
	   
	   String getID(){
		   return friendRecId;
	   }
   }
	
   //comparison class	   
   public static class compareFriends implements Comparator<Object>{
	public int compare(Object o1, Object o2) {
		friendRec friend1 = (friendRec)o1;
		friendRec friend2 = (friendRec)o2;
		int comp = Integer.valueOf(friend2.getNo()).compareTo(Integer.valueOf(friend1.getNo()));
		   
		return comp;
	}
	   
   }
}
   
   