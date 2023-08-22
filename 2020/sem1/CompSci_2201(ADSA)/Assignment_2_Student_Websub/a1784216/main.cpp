#include<stdio.h>
#include<iostream>
using namespace std;

class Node {
	public:
	int data;
	Node* root;
	Node* left;
	Node* right;
	int height;
};

// Get the height of the subtree
int getHeight(Node* node) {
	if (node == NULL) {
		return 0;
	} else {
		return node->height;
	}
}

// Get Balance degree of the current root
int getBalanceDegree(Node *root) {
    if (root == NULL) {
        return 0;
    } else {
    	return getHeight(root->left) - getHeight(root->right);
	}
}

// Get the max integer
int max(int a, int b) {
	if (a > b) {
		return a;
	} else {
		return b;
	}
}  

/* Right Rotation(a)
	 		a            b
	       / \          / \
	      b  T3  --->  T1  a
	     / \              / \ 
	    T1 T2            T2 T3
*/  
Node* rightRotation(Node* a) {
	Node* b = a->left;
	Node* T2 = b->right;
	// Perform rotation
	b->right = a;
	a->left = T2;
	// Alter the heights
	a->height = max(getHeight(a->left), getHeight(a->right)) + 1;
	b->height = max(getHeight(b->left), getHeight(b->right)) + 1;
	// Return current root
	return b;
}

/* Left Rotation(b)
		   b              a
	      / \            / \
	     T1  a   --->   b  T3
	        / \        / \
	       T2 T3      T1 T2
*/
Node* leftRotation(Node* b) {
	Node* a = b->right;
	Node* T2 = a->left;
	// Rotate the node
	a->left = b;
	b->right = T2;
	// Alter the heights  
	b->height = max(getHeight(b->left),getHeight(b->right)) + 1;
	a->height = max(getHeight(a->left),getHeight(a->right)) + 1;
	// Return current root
	return a;
}

// Insert the node and set both left and right of the node to null
Node* insert(int data) {
	Node* node = new Node();
	node->data = data;
	node->left = NULL;
	node->right = NULL;
	node->height = 1;
	return node;
}

// Recursively insert a node in the tree
Node* insertRec(Node* node, int data) {
	// Perform the normal BST insertion
    if (node == NULL) {
        return(insert(data));
    }
  	// Current root > data --> turn left
    if (data < node->data) {
        node->left = insertRec(node->left, data);  
    }
    // Current root < data --> turn right
    else if (data > node->data) {
        node->right = insertRec(node->right, data);  
    }
    // Current root == value, same node is not allowed in the tree so do nothing
    else if (data == node->data) {
    	return node;
    }    
    // Get the height of this parent node
    node->height = max(getHeight(node->left),getHeight(node->right)) + 1;
    // Get the balance degree(v) of the parent node and check whether it is balanced(v=-1,0,1)
    // If it is unbalanced, there are four cases we will meet
    int v = getBalanceDegree(node);  
    // Left Left Case -> parent node do right rotation
    if (v > 1 && data < node->left->data) {
        return rightRotation(node);  
    }
    // Right Right Case -> parent node do left rotation
    if (v < -1 && data > node->right->data) {
        return leftRotation(node);  
    }
    // Left Right Case -> left child of parent node do left rotation -> parent node do right rotation
    if (v > 1 && data > node->left->data) {  
        node->left = leftRotation(node->left);  
        return rightRotation(node);  
    }  
    // Right Left Case -> right child of parent node do right rotation -> parent node do left rotation
    if (v < -1 && data < node->right->data) {  
        node->right = rightRotation(node->right);  
        return leftRotation(node);  
    }
    // return the current root 
    return node;
}

// Find the node with the largest value on the left subtree
Node* findMaxValueNode(Node* node) {
	// First down to the root of the left subtree 
    Node* temp = node->left;  
    // Then loop down to find the node with the largest value(always on the right)
    while (temp->right != NULL) {  
        temp = temp->right;
    }
    return temp;  
}  
  
// Recursively delete a node in the tree 
Node* deleteRec(Node* node, int data) {   
    // Perform the normal BST deletion  
    if (node == NULL) {
        return node;
    }
 	// Current root > data --> turn left
    if (data < node->data) {
        node->left = deleteRec(node->left, data);  
    }
  	// Current root < data --> turn right
    else if(data > node->data) {
        node->right = deleteRec(node->right, data);  
    }
    // Current root == value, which means we find the node to be deleted
  	else if (data == node->data) {
        // Node to be deleted has no child
        if ((node->left == NULL) && (node->right == NULL)) {
            node->left = node;
            node = NULL;
        }
        // Node to be deleted has only one child
        else if ((node->left == NULL) || (node->right == NULL)) {
         // Child is on the right
         if (node->left == NULL) {
            node = node->right;
        // Child is on the left
        } else {
            node = node->left;
        }
        // Node to be deleted has two children 
        } else {  
            // Find the node with the largest value on the left subtree  
            Node* temp = findMaxValueNode(node);  
            // Swap the node to be deleted and the node with the largest value
            node->data = temp->data;  
            // Delete the node  
            node->left = deleteRec(node->left,temp->data);  
        }  
    }   
    // After deletion, if there is no node in the tree, then return the node;  
    if (node == NULL) {
        return node;
    } 
    // Get the height of this parent node
    node->height = max(getHeight(node->left),getHeight(node->right)) + 1;
    // Get the balance degree(v) of the parent node and check whether it is balanced(v=-1,0,1)
    // If it is unbalanced, there are four cases we will meet
    int balance = getBalanceDegree(node);
    // Left Left Case -> parent node do right rotation  
    if (balance > 1 && getBalanceDegree(node->left) >= 0) {
        return rightRotation(node);
    }
    // Right Right Case -> parent node do left rotation 
    if (balance < -1 && getBalanceDegree(node->right) <= 0) {
        return leftRotation(node);
    }
    // Left Right Case -> left child of parent node do left rotation -> parent node do right rotation 
    if (balance > 1 && getBalanceDegree(node->left) < 0) {
        node->left = leftRotation(node->left);
        return rightRotation(node);
    }
    // Right Left Case -> right child of parent node do right rotation -> parent node do left rotation 
    if (balance < -1 && getBalanceDegree(node->right) > 0) {
        node->right = rightRotation(node->right);
        return leftRotation(node);
    }
    return node;
}

void printNode(Node* node, string type) {
    if (node == NULL) {
        return;
    }
    if (type == "PRE") {
        // Root -> left -> right
        cout << node->data << " ";
        printNode(node->left,"PRE"); 
        printNode(node->right,"PRE");
    }
    else if (type == "POST") {
        // Left -> right -> root
        printNode(node->left,"POST");
        printNode(node->right,"POST");
        cout << node->data << " ";
    }
    else if (type == "IN") {
        // Left -> root -> right
        printNode(node->left,"IN");
        cout << node->data << " ";
        printNode(node->right,"IN");
    }
}

int main(int argc, char const *argv[]) {  
    Node *root = NULL;
 	string input;
 	while(cin >> input) {
 		// Check whether input is PRE or POST or IN, if is, print the node and then break the loop
 		if (input == "PRE") {
 			if (root == NULL) {
 				cout << "EMPTY" << endl;
 			} else {
 				printNode(root,"PRE");
 			}
 			break;	
 		}
 		else if (input == "POST") {
 			if (root == NULL) {
 				cout << "EMPTY" << endl;
 			} else {
 				printNode(root,"POST");
 			}
 			break;	
 		}
 		else if (input == "IN") {
 			if (root == NULL) {
 				cout << "EMPTY" << endl;
 			} else {
 				printNode(root,"IN");
 			}
 			break;
 		}
 		// The input is Axx or Dxx
 		else {
 			// Seperate the input into perform(A,D) and data(integer) part
 			char perform = input[0];
 			int data = stoi(input.substr(1,input.size()));
 			// A means insert a node
 			if (perform == 'A') {
 				root = insertRec(root, data);
 			// D means delete a node
 			} else if (perform == 'D') {
 				root = deleteRec(root, data);
 			}
 		}
 	}
}
   




