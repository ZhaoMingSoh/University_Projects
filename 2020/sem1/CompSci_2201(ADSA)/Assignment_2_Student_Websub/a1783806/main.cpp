
#include <iostream>
#include <string>

using namespace std;

//construct node
class Node {
    public:
        int data;
        Node * left;
        Node * right;
        int height;
};

//get the height of the tree
int height(Node * H) {
    if (H == NULL)
        return 0;
    return H -> height;
}

// get maximum integers
int max(int a, int b) {
    return (a > b) ? a : b;
}

// create a new node
Node* newN(int data) {
    Node * node = new Node();
    node -> data = data;
    node -> left = NULL;
    node -> right = NULL;
    node -> height = 1; 
    return node;
}

// rotate the tree to the right
Node * rotateRight(Node * root) {
    Node * node = root -> left;
    Node * temp = node -> right;
    // rotation
    node -> right = root;
    root -> left = temp;
    // update heights
    root -> height = max(height(root -> left),
        height(root -> right)) + 1;
    node -> height = max(height(node -> left),
        height(node -> right)) + 1;
    return node;
}

// rotate the tree to the left in the same manner
Node * rotateLeft(Node * root)
{
    Node * node = root -> right;
    Node * temp = node -> left;
    // rotation
    node -> left = root;
    root -> right = temp;
    // Update heights
    root -> height = max(height(root -> left),
        height(root -> right)) + 1;
    node -> height = max(height(node -> left),
        height(node -> right)) + 1;
    return node;
}

// Get Balance factor
int balFactor(Node * node) {
    if (node == NULL) {
        return 0;
    }
    return height(node -> left) - height(node -> right);
}

// inserrtion
Node * insert(Node * node, int data) {
    // base case
    if (node == NULL) {
        return(newN(data));
    }
    // recursive process
    if (data < node -> data) {
        // insert node on left
        node -> left = insert(node -> left, data);
    }
    else if (data > node -> data) {
        // insert node on right
        node -> right = insert(node -> right, data);
    }
    else {
        return node;
    }
    // update height of node
    node -> height = 1 + max(height(node -> left), height(node -> right)); 
    // get balance for this node
    int balance = balFactor(node);
    
    //unbalanced cases
    // Left Left Case
    if (balance > 1 && data < node -> left -> data) {
        return rotateRight(node);
    }
    // Right Right Case
    if (balance < -1 && data > node -> right -> data) {
        return rotateLeft(node);
    }
    // Left Right Case
    if (balance > 1 && data > node -> left -> data) {
        node -> left = rotateLeft(node -> left);
        return rotateRight(node);
    }
    // Right Left Case
    if (balance < -1 && data < node -> right -> data) {
        node -> right = rotateRight(node -> right);
        return rotateLeft(node);
    }
    return node;
}

// return max value of node
Node* maxNode(Node* node) {
    Node* temp = node;
    while (temp -> right != NULL) {
        temp = temp -> right;
    }
    return temp;
}

// deletion
Node * deleteNode(Node * root, int data) {
    // base case
    if (root == NULL) {
        return root;
    }
    // recursive process
    if (data < root -> data) {
        root -> left = deleteNode(root -> left, data);
    }
    else if (data > root -> data) {
        // delete node from right
        root -> right = deleteNode(root -> right, data);
    }
    else {
        // node with only 1 child
        if ((root -> left == NULL) || (root -> right == NULL)) {
            Node * temp = root -> left;
            if (temp == NULL) {
                temp = root -> right;
            }
            // temp does not have children
            if (temp == NULL) {
                temp = root;
                root = NULL;
            }
            else {
                *root = *temp;
            }
            delete temp;
        }
        else {
            // node have both children
            Node* temp = maxNode(root -> left);
            // copy data to root node
            root -> data = temp -> data;
            // delete node from left side
            root -> left = deleteNode(root -> left, temp -> data);
        }
    }
    if (root == NULL) {
        return root;
    }
    // update height
    root -> height = 1 + max(height(root -> left), height(root -> right));
    // get balance of current node
    int balance = balFactor(root);

    // Again, unbalanced cases
    // Left Left Case
    if (balance > 1 && balFactor(root ->left) >= 0) {
        return rotateRight(root);
    }
    // Left Right Case
    if (balance > 1 && balFactor(root -> left) < 0) {
        root -> left = rotateLeft(root -> left);
        return rotateRight(root);
    }
    // Right Right Case
    if (balance < -1 && balFactor(root -> right) <= 0) {
        return rotateLeft(root);
    }
    // Right Left Case
    if (balance < -1 && balFactor(root -> right) > 0) {
        root->right = rotateRight(root -> right);
        return rotateLeft(root);
    }
    return root;
}

// pre order
void preOrder(Node* root) {
    if (root != NULL) {
        cout << root->data << " ";
        preOrder(root->left);
        preOrder(root->right);
    }
}
// post order
void postOrder(Node* root) {
    if (root != NULL) {
        postOrder(root->left);
        postOrder(root->right);
        cout << root->data << " ";
    }
}
// in order
void inOrder(Node* root) {
    if (root != NULL) {
        inOrder(root->left);
        cout << root->data << " ";
        inOrder(root->right);
    }
}


int main() {
    // initialize AVL tree
    Node* root = NULL;
    string token;
    // get user input till they enter nish move
    while (cin >> token) {
        // check for nish move
        if (token.compare("IN") == 0) {
            cout << " ";
            // print tree in order
            if (root == NULL) {
                cout << "EMPTY" << endl;
            }
            else {
                inOrder(root);
            }
            // break the loop as we found nish move
            break;
        }
        else if (token.compare("PRE") == 0) {
            cout << " ";
            // print tree in pre order
            if (root == NULL) {
                cout << "EMPTY" << endl;
            }
            else {
                preOrder(root);
            }
            // break the loop as we found nish move
            break;
        }
        else if (token.compare("POST") == 0) {
            cout << " ";
            // print tree in post order
            if (root == NULL) {
                cout << "EMPTY" << endl;
            }
            else {
                postOrder(root);
            }
            // break the loop as we found nish move
            break;
        }
        else {
            // token is add or delete instruction
            int value = stoi(token.substr(1, token.size()));
            // check for add node
            if (token[0] == 'A') {
                root = insert(root, value);
            }
            // check for delete node
            else if (token[0] == 'D') {
                root = deleteNode(root, value);
            }
            // do nothing for invalid input
        }
    }
    cout << endl;
    return 0;
}

