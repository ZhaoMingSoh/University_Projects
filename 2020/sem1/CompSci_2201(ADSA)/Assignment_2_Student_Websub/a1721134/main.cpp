#include <iostream>
#include <string>
#include <sstream>
#include <vector>

using namespace std;

class Node
{
//each node has these public attributes
public:
	
	int value;
	int height;
	Node *left;
	Node *right;
	
	
};

//new node is created with given value and NULL pointers and height 1
Node* newNode(int value){

	Node* node = new Node();
	node->value=value;
	node->left=NULL;
	node->right=NULL;
	node->height=1;

	return(node);

}

//function to return height
int height(Node *N){

	if (N==NULL)
	{
		return 0;

	}

	return N->height;
}

//function to return the balance of the tree
int getbalance(Node *n){

	if (n==NULL)
	{
		return 0;
	}

	return height(n->left)-height(n->right);
}

//returns the max value between 2 integars
int max(int a,int b){

	if (a>b)
	{
		return a;
	}

	else return b;
	//return (a > b)? a : b;
}

// returns the largest node on the left branch to handle 2 children case
Node *largestNode(Node* node){

	Node* current = node;

	while(current->right!=NULL){
		current = current->right;
	}

	return current;
}

//right rotation for balance
Node *rightrotation(Node *y){

    

    	Node *x = y->left;
    	Node *temp=x->right;
    	
    	x->right = y;
    	y->left = temp;
    
    	y->height = max(height(y->left), height(y->right))+1;
    	x->height = max(height(x->left), height(x->right))+1;

    	return x;

}


//left rotation for balance
Node *leftrotation(Node *x){


    	Node *y = x->right;
    	Node *temp = y->left;
    	

    	y->left = x;
    	x->right = temp;
    
    	x->height = max(height(x->left), height(x->right))+1;
    	y->height = max(height(y->left), height(y->right))+1;

    	return y;


}

//right left case rotation
Node *doubleleft(Node *y){

	
	y->right = rightrotation(y->right);
	return leftrotation(y);
}

//left right case rotation
Node *doubleright(Node *y){
	
	y->left = leftrotation(y->left);
	return rightrotation(y);
}


Node *insert(Node *node, int value){

	//first node
	if (node == NULL)
	{
		return (newNode(value));
	}

	//inserted left or right depending on value
	else if (value < node->value)
	{
		node->left = insert(node->left,value);
		
	}

	else if (value > node->value)
	{
		node->right = insert(node->right,value);

	}

	else
		return node;

	//height is updated
	node->height = max(height(node->left), height(node->right))+1;

	//rotation functions are called depending on particular cases
	int balance = getbalance(node);

	if (balance>1 && value < node->left->value){
		return rightrotation(node);
	}

	if (balance<-1 && value > node->right->value)
	{
		return leftrotation(node);
	}

	if (balance>1 && value > node->left->value)
	{
		
		return doubleright(node);
	}

	if (balance<-1 && value < node->right->value)
	{
		return doubleleft(node);
	}


   	return node;

}

Node *removeNode(Node *node, int value){

    Node* temp;

    if (node==NULL)
    {
        return node;
    }

    //deleted from left or right node based on value
    if(value < node->value){
        node->left = removeNode(node->left,value);
    }

    else if(value > node->value){
        node->right = removeNode(node->right,value);
    }


    else 
    {
        //single child node or no child
        if(node->left == NULL || node->right == NULL){

        Node *temp = node->left ? node->left : node->right;  

        
        //no child
        if (temp==NULL)
        {
        temp=node;
        node=NULL;
        }

        //single child
        else
            *node=*temp;

        delete temp;
        }

        //node with 2 children, gets replaced with largest in right sub tree
        else 
        {
        temp = largestNode(node->left);
        node->value = temp->value;
        node->left = removeNode(node->left,temp->value);
        }

    }

    

    if (node == NULL)
    {
        return node;
    }

    node->height = max(height(node->left),height(node->right))+1;

    int balance = getbalance(node);

    //balance is restored based on given conditions 
    if (balance>1 && getbalance(node->left)>=0)
    {
        return rightrotation(node);
    }

    if (balance>1 && getbalance(node->left)<0)
    {
        
        return doubleright(node);
    }

    if (balance<-1 && getbalance(node->right)<=0)
    {
        return leftrotation(node);
    }

    if (balance<-1 && getbalance(node->right)>0)
    {
        
        return doubleleft(node);
    }

    return node;

}


//preorder treversal
void preOrder(Node *root){

	if (root != NULL)
	{
		cout << root->value << " ";
		preOrder(root->left);
		preOrder(root->right);
	}
}

//postorder treversal
void postOrder (Node *root){

	if (root != NULL)
	{
		
		postOrder(root->left);
		postOrder(root->right);
		cout << root->value << " ";
	}

}

//postorder treversal
void inOrder (Node *root){

	if (root != NULL)
	{
		
		inOrder(root->left);
		cout << root->value << " ";
		inOrder(root->right);
	}
}

int main()
{

	string input;
	string command;
	string value;
	vector<int> integers;

	//root is created as a NULL pointer
	Node *root = NULL;

	getline(cin, input);

	//loops through entire input
	for (int i = 0; i < input.length(); ++i)
    {
        
        //a string is created with each command (A or D) 
        if(isalpha(input[i]) ){
            
            command += input[i];
            int k = i+1;
            
            // a vector is created with all the numbers following each command
            while(isdigit(input[k])){
                
                
                value += input[k];
                k++;
                
            }

            if (value!="")
            {
                integers.push_back(stoi(value));
            }  
            
            value = "";

        }

    }
	

	//insert or delete function called based on command
	for (int i = 0; i < integers.size(); ++i)
	{
		if (command[i]=='A')
		{
			int k = integers[i];
			root = insert(root, k);
		}

		else if (command[i]=='D')
		{
			int k = integers[i];
			root = removeNode(root, k);
		}

	}

	//treversal functions called based on last letter of input
	if (command.back()=='E')
	{
		if(root == NULL)
		{
			cout << "EMPTY";
		}

		else

		preOrder(root);
		cout << endl;
	}

	else if (command.back()=='N')
	{

		if(root == NULL)
		{
			cout << "EMPTY";
		}

		else

		inOrder(root);
		cout << endl;
	}

	else if (command.back()=='T')
	{
		
		if(root == NULL)
		{
			cout << "EMPTY";
		}

		else

		postOrder(root);
		cout << endl;
	}

	return 0;
	
}