
#include <iostream>
#include <vector>
#include <sstream>
#include <string>
#include <algorithm>
#include <cassert>
#include <cmath>


// function to take a line of user input and return it as a
// vector containing each word separated by a space as elements
std::vector<std::string> get_input() {
	
	// get and store a line of user input	
	std::string input;
	std::getline(std::cin, input);

	// catch empty input string
	if (input.size() < 1) {
		throw -1;
	}

	// vector to hold the input names of the players (expected 8)
	std::vector<std::string> output;

	// transform the input into a string stream to iterate over and declare a temp storage string
	std::stringstream inp_stream(input);
	std::string temp;

	// loop through the words in the input stream separated by a space
	while(std::getline(inp_stream, temp, ' ')) {
		// add each word to the end of the output vector 
		output.push_back(temp);
	}

	return output;

}

// helper function to make sure two strings are of equal length by appending leading zeroes
// extends the shorter string with leading zeroes and returns the new shared length
int check_length(std::string* a, std::string* b) {

	int diff = 0;
	// if a is longer than b, extend b
	if (a->length() > b->length()) {
		
		// calculate the difference between the two strings and fix the length of the shorter string
		diff = a->length() - b->length();
		*b = std::string(diff, '0') + *b;

	// if b is longer than a, extend a
	}else if(b->length() > a->length()) {
		
		// calculate the difference between the two strings and fix the length of the shorter string
		diff = b->length() - a->length();
		*a = std::string(diff, '0') + *a;

	}

	// ensure the two lengths are the same
	assert(a->length() == b->length());

	return a->length();


}



// school method algorithm for computing the sum of two inputs
// takes two input strings of digits and the base to perform them in
std::string school_sum(std::string inp1, std::string inp2, std::string B) {
	
	// declare variables 
	std::string output = "";
	int carry = 0;
	int base = std::stoi(B);

	// ensure the two inputs have the same number of digits by adding leading zeroes
	int length = check_length(&inp1, &inp2);

	// from the end of l2, loop back adding each element 
	for (int i = length - 1; i >= 0; --i) {

		// add the elements, from right hand side of the string and the carry digit
		int sum = std::stoi(std::string(1, inp2[i])) + std::stoi(std::string(1, inp1[i])) + carry;

		//operations are applied in terms of the specified base system

		// add the least signifigant digit of the sum to the output string
		output += std::to_string(sum % base);

		// add the most signifigant digit of the sum to the carry 
		carry = sum / base;

	}

	// if there is a remaining carry digit, add it to the end of the string
	if (carry != 0) {
		output += std::to_string(carry);
	}

	// reverse the final output so MSD is on left side as standard 
	std::reverse(output.begin(), output.end());

	return output;


}

// subtraction of two ints by school method, performs inp1 - inp2
// takes two input strings of digits and the base to perform them in
// function assumes the first input is always larger than the second, (valid for katasuba w/ non-negative ints) so never returns a negative result
std::string school_diff(std::string inp1, std::string inp2, std::string B) {
	
	// declare variables 
	std::string output = "";
	int carry = 0;
	int base = std::stoi(B);
	
	// ensure the two inputs have the same number of digits by adding leading zeroes
	int length = check_length(&inp1, &inp2);

	// from the end of l2, loop back subtracting each element 
	for (int i = length - 1; i >= 0; --i) {


		// subtract the elements, from right hand side of the string and the carry digit (if present from last subrtaction)
		int diff = std::stoi(std::string(1, inp1[i])) - std::stoi(std::string(1, inp2[i])) - carry;


		//operations are applied in terms of the specified base system
		// if the difference will influence a neighbouring digit, add the base value and subtract one from next MSB
		// append resulting digit to the output string
		if (diff < 0) {
			output += std::to_string(diff + base);
			carry = 1;

		}else {
			output += std::to_string(diff);
			// reset carry digit before next subtraction
			carry = 0;

		}

	}

	// reverse the final output so MSD is on left side as standard 
	std::reverse(output.begin(), output.end());

	return output;


}

// single digit multiplication in base B
std::string school_mult(std::string inp1, std::string inp2, std::string B) {

	// declare variables 
	std::string output = "";
	std::string sum = "";
	int carry = 0;
	int k = 0;
	int base = std::stoi(B);

	// ensure the two inputs have the same number of digits by adding leading zeroes
	int length = check_length(&inp1, &inp2);

	// loop along from the least signifigant digit (rightmost) of input 2
	for (int j = length-1; j >= 0; --j) {

		// reset sum and carry after each multiplier
		sum = "";
		carry = 0;

		// loop through each element of input 1 for each element of input 2
		for (int i = length-1; i >= 0; --i) {
			
			// multiply the two elements and add any carry over digit
			int prod = std::stoi(std::string(1, inp1[i])) * std::stoi(std::string(1, inp2[j])) + carry;

			//operations are applied in terms of the specified base system

			// add the least signifigant digit of the prod to the sum string
			sum += std::to_string(prod % base);

			// add the most signifigant digit of the prod to the carry 
			carry = prod / base;
		}

		// if there is a remaining carry digit, add it to the end of the string
		if (carry != 0) {
			sum += std::to_string(carry);
		}

		// reverse the digits of the sum string and append trailing zeroes relative to the base 
		// i.e. for each sum the base power increases by one (1's, 10's, 100's etc) 
		std::reverse(sum.begin(), sum.end());
		sum += std::string(k, '0');
		k++;

		// add the sum to the running output sum (using school addition in same base)
		output = school_sum(output, sum, B);

	}
	
	return output;



}

//function to find the product of two ints with karatsuba multiplication algorithm in a specified base 
// takes three non negative integer strings, two inputs and a system base 
std::string karatsuba(std::string inp1, std::string inp2, std::string B) {

	// ensure the two inputs have the same number of digits by adding leading zeroes
	int length = check_length(&inp1, &inp2);

	// base case, zero length input
	if (length == 0) {
		
		return "0";

	// base case, for three dgit inputs or less use school method of multiplication  
	}else if(length <= 3){

		return school_mult(inp1, inp2, B);

	}else {

		// subdivide input into two partitions, 
		// k0 with the least signifigant digits (rounding down), k1 with the remaining (most signifigant)
		int k0 = std::floor(length/2);
		int k1 = length - k0;

		// split each input into its two substrings 
		std::string a1 = inp1.substr(0, k1);
		std::string a0 = inp1.substr(k1, inp1.length());

		std::string b1 = inp2.substr(0, k1);
		std::string b0 = inp2.substr(k1, inp2.length());

		// all operations performed in input base B

		// recursively calculate karatsuba products 
		// a0 x b0,		a1 x b1, 	(a0 + a1)x(b0 + b1).
		std::string p0 = karatsuba(a0, b0, B);
		std::string p1 = karatsuba(school_sum(a0, a1, B), school_sum(b0, b1, B), B);
		std::string p2 = karatsuba(a1, b1, B);

		// calculate the difference (p1 - (p2 + p0)) and append zeroes to the end of each product as required
		// using school method for summation and subtraction
		std::string out1 = p2 + std::string(k0*2, '0');
		std::string out2 = school_diff(p1, school_sum(p0, p2, B), B) + std::string(k0, '0');
		std::string out3 = p0; 

		// sum the three outputs together using school method
		std::string output = school_sum(school_sum(out1, out2, B), out3, B);

		// remove leading zeroes, catch case for single digit, zero output (remains 0 not empty string)
		output.erase(0, std::min(output.find_first_not_of('0'), output.length() - 1));

		return output;


	}


}


int main() {

	// receive inout from command line and store as a vector of strings, each element delimited by a space
	std::vector<std::string> input = get_input();

	// print the sum of the two elements and their karatsuba product, in input base
	std::cout << school_sum(input[0], input[1], input[2]) << " " << karatsuba(input[0], input[1], input[2]) << std::endl;


	return 0;

}










