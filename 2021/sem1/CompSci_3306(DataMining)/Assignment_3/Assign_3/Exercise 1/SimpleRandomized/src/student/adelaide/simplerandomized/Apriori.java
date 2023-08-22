package student.adelaide.simplerandomized;

import java.io.*;
import java.util.*;

public class Apriori extends Observable {
	
	private List<int[]> itemsets;
	private String transaFile;
	private int numItems;
	private int numTransactions;
	private double minSup;
	private FileWriter fw;
	
	
	public Apriori(String inFile, String outFile, double s) throws Exception
	{
		transaFile = inFile;
		minSup = s; //set support threshold (as percentage of total transactions)
		fw = new FileWriter(outFile);
		intitialiseSettings();
	}
	
	public void startPasses() throws Exception {
		itemsets = new ArrayList<int[]>();
		for (int i=0; i<numItems;i++) {
			int[] candidate = {i};
			itemsets.add(candidate);
		}
		int currentSet = 1;
		int frequentSetCount = 0;
		while(itemsets.size()>0){
			System.out.print("Checking set size " + currentSet + "... ");
			//System.out.println("itemset size: " + Integer.toString(itemsets.size()));
			calculateFrequentItemSets();
			System.out.print("Found " + itemsets.size() + " frequent sets.\n");
			if (itemsets.size()!=0){
				frequentSetCount+=itemsets.size();
				generateCandidates();
			}
			currentSet++;
			
		}
		System.out.println("Completed search for itemsets. Found " + frequentSetCount);
		fw.close();
	}
	
	private void generateCandidates()
	{
		int itemsetSize = itemsets.get(0).length;
		HashMap<String, int[]> tempCandidates = new HashMap<String, int[]>();
		for(int i=0;i<itemsets.size();i++){
			for(int j=i+1;j<itemsets.size();j++){
				
				int[] newCandidate = new int[itemsetSize+1];
				int[] X = itemsets.get(i);
				int[] Y = itemsets.get(j);
				
				
				for(int s=0;s<newCandidate.length-1;s++){
					newCandidate[s] = X[s];
				}
				
				int differencesCount = 0;
				for(int m=0;m<Y.length;m++) {
					boolean found = false;
					for(int n=0;n<X.length;n++){
						if(X[n] == Y[m]){
							found = true;
							break;
						}
					}
					if(!found){
						differencesCount++;
						newCandidate[newCandidate.length-1] = Y[m];
					}
				}
				
				if(differencesCount==1){
					Arrays.sort(newCandidate);
					tempCandidates.put(Arrays.toString(newCandidate), newCandidate);
				}
				
			}	
		}
		
		itemsets = new ArrayList<int[]>(tempCandidates.values());
	}
		
	private void calculateFrequentItemSets() throws Exception
	{
		BufferedReader data_in = new BufferedReader(new FileReader(transaFile));
		List<int[]> frequentCandidates = new ArrayList<int[]>();
		boolean match;
		int count[] = new int[itemsets.size()];
		boolean[] trans = new boolean[numItems];
		
		for (int i=0;i<numTransactions;i++) {
			String row = data_in.readLine();
			
			Arrays.fill(trans, false);
			StringTokenizer t = new StringTokenizer(row," ");
			while(t.hasMoreTokens()) {
				int x = Integer.parseInt(t.nextToken());
				trans[x] = true;
			}
			
			for(int c=0;c<itemsets.size();c++) {
				match = true;
				int[] candidate = itemsets.get(c);
				for(int y: candidate){
					if(trans[y] == false){
						match = false;
						break;
					}
				}
				if(match){
					count[c]++;
				}
			}	
		}
		data_in.close();
		
		for (int i=0;i<itemsets.size();i++)
		{
			if((count[i]/(double)numTransactions) >= minSup) {
				frequentCandidates.add(itemsets.get(i));
				//System.out.println(Arrays.toString(itemsets.get(i)) + " ("+((count[i]/(double) numTransactions)) + " " + count[i]+")" + Double.toString(numItems));
				//System.out.println("initial settings. minSup: " + Double.toString(minSup) + " numItems: " + Double.toString(numItems));
				fw.write(Arrays.toString(itemsets.get(i)) + " ("+((count[i]/(double) numTransactions)) + " " + count[i]+")\n");
			}
		}
		itemsets = frequentCandidates;
	}
	
	private void intitialiseSettings() throws Exception
	{
		numItems = 0;
		numTransactions = 0;
		BufferedReader data_in = new BufferedReader(new FileReader(transaFile));
		while(data_in.ready()) 
		{
			String row = data_in.readLine();
			if(row.matches("//s*")) continue; //skip empty lines
			numTransactions++;
			StringTokenizer t = new StringTokenizer(row," ");
			while(t.hasMoreTokens()) {
				int x = Integer.parseInt(t.nextToken());
				if(x+1 > numItems) {
					numItems = x+1;
				}
			}
		}
		data_in.close();
		//System.out.println("intial seetings. minSup: " + Double.toString(minSup) + " numItems: " + Double.toString(numItems));
		
		
		
	}

}
