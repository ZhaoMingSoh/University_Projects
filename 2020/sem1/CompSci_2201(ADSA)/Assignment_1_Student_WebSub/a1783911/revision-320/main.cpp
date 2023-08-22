#include <iostream> 
#include <string> 
#include <sstream> 
#include <vector>
#include <math.h>
using namespace std;

/*
* @function reverseStr This function reverses the string.
* @param str The pointer to the input string
* @return null
*/
void reverseStr(string& str) 
{ 
    int n = str.length(); 

    // Swap character starting from two 
    // corners 
    for (int i = 0; i < n / 2; i++) 
        swap(str[i], str[n - i - 1]); 
}


/*
* @class Base   This class is used to store the numbers in an array form. This class also stores
                the number of the digits in the number and its value in string format.
*/
class Base{
    public:
        //Initializing class level varibales.
        vector<int> digits; //Stores the digits in array format
        int length; //Stroes the lenght of the string (Number)
        string value; //Stores the value of the number.

        Base(string number, int baseNumber) {
            length = number.length();
            value = number;

            //Loop throught the string and store the charcacters in an array
            for (int i = length - 1; i >= 0; i--) {
                digits.push_back(number[i] - '0');
            }
        };
};


/*
* @class Add   This class adds the two numbers using school method. It takes the input as 2 numbers as a Base class object and the base of the numbers.
                And returns the sum of two numbers in string format
*/
class Add{

    public:
        //Initalizing the class level variables
        Base *firstNumber;
        Base *secondNumber;
        vector<int> sumPartials; //used to store the partials
        int sum = 0;
        int carry = 0; //Initialize the carry to zero
        int base;

        //Constructor to intialize the class level variables.
        Add(Base *first, Base *second, int baseOfNumbers) {
            firstNumber = first;
            secondNumber = second;
            base = baseOfNumbers;
        };

        /*
        * @function performAddition     This function performs the addition of the two numbers stored in class level
        *                               variables.
        * @param null
        * @return string    The result of the addition.
        */
        string performAddition() {
            //declare varibales
            int len; //Stores the length of the smaller number
            Base *largerNumber;

            //Checking which number is greater. If the first one is smaller then store its length in the
            //len variable. else do it for the second one.
            if(firstNumber->length < secondNumber->length) {
                len = firstNumber->length;
                largerNumber = secondNumber;
            } else {
                len = secondNumber->length;
                largerNumber = firstNumber;
            }

            //Loop through both the numbers till the length of the smaller number and add the digits - bit by bit.
            for(int index = 0; index < len; index++) {
                //Add the current digits of both the numbers along with the carry of the perivous digit's addition.
                int sum = carry + firstNumber->digits[index] + secondNumber->digits[index];
                //push the resultant digit in to the partials vector.
                sumPartials.push_back(sum % base);
                //calculate the carry
                carry = sum / base;
            }

            //Now if the numbers are of different lenths and there is an overflow, then add the overflow to the partials.
            if(firstNumber->length == secondNumber->length && carry != 0) {
                sumPartials.push_back(carry);
            } else if (firstNumber->length != secondNumber->length) {

                //If the numbers are not of different lengths then we need to add the
                //remaining digits of the larger number to the partials vector along with the
                //carry, if any.
                int start = sumPartials.size();

                //Lopp theough the remaing digits of the larger number bit by bit. Perform addition of
                //each bit with the carry fo the prvious addition and store the result to the partials vector.
                for(int index = start; index < largerNumber->length; index++) {
                    int tempSum = largerNumber->digits[index] + carry;
                    sumPartials.push_back(tempSum % base);
                    carry = tempSum / base;
                }

                //By doing the aboove activity if there still remains an overflow then add it to the partials vector.
                if(carry != 0) {
                    sumPartials.push_back(carry);
                }
            }

            //resultant string
            string result = "";
            //Loop though the partials vector and add them through to the result string
            for (int index = 0; index < sumPartials.size(); index++) {
                result = to_string(sumPartials[index]) + result;
            }
            return result;
        }

        /*
        * @function displayResult   This function dispalys the result of the addition on console.
        * @param null
        * @return null
        */

        void displayResult() {
            //Loop through the partials array, backwards, and diplay the result on console.
            for(int index = sumPartials.size() - 1 ; index >= 0 ; index--)    
            {    
                cout << sumPartials[index];
            }
        }
};


/*
* @class Subtract   This class subtracts the two given numbers using school method. it takes 2 numbers, objects of Base class, and the base
                    of the numbers, as an input. Result is the difference of the two numbers in string format.
*/
class Subtract
{
public:
    //declare class level variables.
    Base *firstNumber;
    Base *secondNumber;
    int base;

    //Constructor to initialze class level varibales.
    Subtract(Base *first, Base *second, int baseOfNumbers){
        firstNumber = first;
        secondNumber = second;
        base = baseOfNumbers;
    }
    
    /*
    * @function subtractNumbers     This function subtracts the two numbers stored in class.
    * @param null
    * @return string    The result of the subtraction.
    */
    string subtractNumbers() {

        //storing the length of both the numbers.
        int l1 = firstNumber->value.length();
        int l2 = secondNumber->value.length();

        //declaring some more variables
        string result = "";
        int carry = 0; //initialze the carry to zero

        Base *largerNum;
        Base *SmallerNum;

        //Checking which number is larger and which one is smaller and caching it accordingly.  
        if(l1 < l2) {
            largerNum = secondNumber;
            SmallerNum = firstNumber;
        } else {
            largerNum = firstNumber;
            SmallerNum = secondNumber;
        }

        //Stroing the numbers in string format.
        string largerStr = largerNum->value;
        string smallerStr = SmallerNum->value;

        //Reversing both the strings 
        reverseStr(largerStr);
        reverseStr(smallerStr);
        
        //Looping botthe numbers till the length of smaller number and subtracting both of them bit by bit, along
        //with the carry, if any.
        for(int index = 0; index < smallerStr.length(); index++) {
            //compute difference of current digits 
            int diff = ((largerStr[index]-'0')-(smallerStr[index]-'0')-carry); 

            // If difference is negative then we add base to it and intialize carry to 1 for future calculations
            if (diff < 0)
            { 
                diff = diff + base; 
                carry = 1; 
            } 
            else
                carry = 0; 

            //storing the difference in result string
            result.push_back(diff + '0'); 
        }

        //Now if the number of digits of both the numbers are not same then we need to looping throught
        //the remaing digits of the larger number and accounth them in result string
        for (int index = smallerStr.length() ; index < largerStr.length(); index++) 
        {   
            //Compting the difference of current digit along with the carry of previous subtraction
            int diff = ((largerStr[index]-'0') - carry); 
            
            // If difference is negative then we add base to it and intialize carry to 1 for future calculations
            if (diff < 0)
            { 
                diff = diff + base; 
                carry = 1; 
            } 
            else
                carry = 0; 
            
            //storing the difference in result string
            result.push_back(diff + '0'); 
        } 
    
        // reverse resultant string 
        reverseStr(result); 
    
        return result;
    }
};


/*
* @class Multiplication   This class mutiplies two given numbers using karatsuba algorithm. It takes 2 numbers,objects of Base class, and the base
                          of the numbers, as an input. result is the multipcation of the two numbers in string format.
*/
class Multiplication
{
public:
    //Declare the variables
    Base *firstNumber;
    Base *secondNumber;
    int base;
    int a[2]; //Used to store the two halves of the first number.
    int b[2]; //used to store the two halves of the second number.
    int partial[3]; //used to store the partials of the mutiplication
    int k; //constant factor by which we divides the number.

    //Parameterized constructor to intialize the variables.
    Multiplication(Base *first, Base *second, int baseOfNumbers) {
        firstNumber = first;
        secondNumber = second;
        base = baseOfNumbers;
    }

    /*
    * @function singlebitMultiplication     This function mutiplies the 2 - one bit digits.
    * @param lhs    The first bit
    * @param rhs    The second bit
    * @return string   The result of the multiplication.
    */
    string singlebitMultiplication(char lhs, char rhs) {
        //mutiply both the bits.
        int mul = (lhs-'0')*(rhs-'0');
        //check the size of the result.
        int size = to_string(mul).length();

        string res = "";
        //take the modulus of the result with the base to get the digit at one's place.
        res = to_string(mul % base);

        //divide the result by base to check if the result was greater than the base. if it is then we need
        //to add the overflow to the result.
        int carry = mul/base;
        //If there is an overflow then add it to the result.
        res = carry != 0 ? to_string(carry) + res : res;

        return res;
    }


    /*
    * @function multiply     This function mutiplies the 2 numbers using karatsuba. This function recurssively divides the
    *                        the number into the 
    * @param lhs    The first bit
    * @param rhs    The second bit
    * @return string   The result of the multiplication.
    */
    string multiply(string lhs, string rhs) {
        //Declaring variables
        int length;
        vector <string> partials;

        //Checking which of the two numbers is bigger. The biggest length will be stored in the variable.
        if (lhs.size() > rhs.size())
        {
            length = lhs.size();
        } else {
            length = rhs.size();
        }
        
        //adding zero's in front of the number if its length is smaller than the other.
        while (lhs.size() < length) {
            lhs.insert(0,"0");
        }
        
        while (rhs.size() < length) {
            rhs.insert(0,"0");
        }

        //If the number is of single bit then finding its multiplication.
        if (length == 1){
            return singlebitMultiplication(lhs[0],rhs[0]);
        }

        //spliting both the numbers in halves and storing the leading and trailing parts to the corresponding variables.
        //The number at 0th index contains the leading part while the number at 1st index conatins the traling part.
        string a0 = lhs.substr(0,length/2);
        string a1 = lhs.substr(length/2,length-length/2);
        string b0 = rhs.substr(0,length/2);
        string b1 = rhs.substr(length/2,length-length/2);

        //Converting the numbers into the objects of Base class.
        Base *lhs0 = new Base(a0,base);
        Base *lhs1 = new Base(a1,base);
        Base *rhs0 = new Base(b0,base);
        Base *rhs1 = new Base(b1,base);

        //Adding the numbers using Add class.
        Add *lh = new Add(lhs0, lhs1, base);
        Add *rh = new Add(rhs0, rhs1, base);

        //storing the partials in the partial vector
        partials.push_back(multiply(a0,b0)); // partial p0 --> a0 * b0
        partials.push_back(multiply(a1,b1)); // Partial p1 --> a1 * b1
        partials.push_back(multiply(lh->performAddition(),rh->performAddition())); //Partial p2 --> (a0 + a1) * (b0 + b1)

        Base *par0 = new Base(partials[0],base);
        Base *par1 = new Base(partials[1],base);

        Add *partial = new Add(par0,par1,base);
        Subtract *subPartial = new Subtract(new Base(partials[2],base), new Base(partial->performAddition(), base), base);

        string diff = subPartial->subtractNumbers();
        partials.push_back(diff); //Partial p3 --> (p1 - (p2 + p0))

        //Apending zero's in front of partils if thier length is less than the spliting factor
        for (int i = 0; i < 2*(length-length/2); i++)
            partials[0].append("0");
        for (int i = 0; i < length-length/2; i++)
            partials[3].append("0");

        Base *x = new Base(partials[0],base);
        Base *y = new Base(partials[1],base);
        Base *z = new Base(partials[3],base);

        Add *d = new Add(x,y,base);
        Add *r = new Add(new Base(d->performAddition(),base),z,base);

        string result = r->performAddition();

        return result.erase(0, min(result.find_first_not_of('0'), result.size()-1));
    }
};


/*
* @function main This is the main function which runs when this files gets compiled.
* @param null
* @return null
*/
int main(){
    //Declaring variables
    string first , second;
    int base;

    //Getting inputs from the command line and storing them in variables.
    cin >> first >> second >> base;

    //Making the numbers as objects of base class.
    Base *firstNumber = new Base(first,base);
    Base *secondNumber = new Base(second,base);

    //Adding the two given numbers
    Add *addition = new Add(firstNumber, secondNumber, base);
    addition->performAddition(); //Performing addition
    addition->displayResult(); //Displaying the result of addition
    cout << " ";

    //Multiplying the two numbers.
    Multiplication *mul = new Multiplication(firstNumber, secondNumber, base);
    cout << mul->multiply(firstNumber->value, secondNumber->value);
}