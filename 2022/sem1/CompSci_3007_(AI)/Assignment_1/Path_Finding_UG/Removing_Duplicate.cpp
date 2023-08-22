#include <iostream>
#include <algorithm> 
#include <vector>
using namespace std;

// void remove_duplicates(int* arr, int& n) {

// 	int k = 0;

// 	// iterate each element of arr[]
// 	for (int i = 0; i < n; ++i) {

// 		// When there the elements arr[j] != arr[i] 
//         // (j will always be smaller than i because it compares all the left elements j to the current element i)
// 		int flag = false;
// 		for (int j = 0; j < i; ++j) {
// 			if (arr[j] == arr[i]) {
// 				flag = true;
// 				break;
// 			}
// 		}

// 		if (flag == false) {
//             swap (arr[k++], arr[i]);
// 			// int temp = arr[k];
//             // arr[k] = arr[i];
//             // arr[i] = temp;
//             // k++;
//             cout << "k :" << k << ", i : " << i << endl;
//             for(int i = 0; i<n; i++){
//                 cout << arr[i] << " ";
//             }
//             cout << endl;
//         }

// 	}

// 	n = k;

// }

// void remove_duplicate_via_pointer(int* arr, int& n){
//      // Both pointers start from index 1 because the first value is always a unique value.
//     int left_pointer = 1;
//     for(int right_pointer=1; right_pointer<n; ++right_pointer){
//         if(arr[right_pointer] != arr[right_pointer-1]){
//             arr[left_pointer] = arr[right_pointer];
//             left_pointer++;
//         }
//     }

//     n = left_pointer;
// }

// int main() {

// 	int arr[] = {2,1,4,2};
//     int n = sizeof(arr) / sizeof(int);
//     sort(arr,arr+n);

// 	cout << "Input Array: ";
// 	for (int i = 0; i < n; ++i)	cout << arr[i] << ' ';
// 	cout << endl;

// 	// remove_duplicates(arr, n);
//     remove_duplicate_via_pointer(arr, n);

// 	cout << "Output Array: ";
// 	for (int i = 0; i < n; ++i)	cout << arr[i] << ' ';
// 	cout << endl;
// }
