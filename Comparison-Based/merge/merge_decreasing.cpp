#include <iostream>
using namespace std;

// Function to merge two subarrays in decreasing order
void merge(int arr[], int left, int mid, int right) {
    int n1 = mid - left + 1;  // Size of the left subarray
    int n2 = right - mid;     // Size of the right subarray

    // Create temporary arrays for left and right subarrays
    int leftArr[n1], rightArr[n2];

    // Copy data to temporary arrays
    for (int i = 0; i < n1; i++) {
        leftArr[i] = arr[left + i];
    }
    for (int i = 0; i < n2; i++) {
        rightArr[i] = arr[mid + 1 + i];
    }

    // Merge the temporary arrays back into the original array in decreasing order
    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (leftArr[i] >= rightArr[j]) {  // Change the comparison for decreasing order
            arr[k] = leftArr[i];
            i++;
        } else {
            arr[k] = rightArr[j];
            j++;
        }
        k++;
    }

    // Copy any remaining elements from the left subarray
    while (i < n1) {
        arr[k] = leftArr[i];
        i++;
        k++;
    }

    // Copy any remaining elements from the right subarray
    while (j < n2) {
        arr[k] = rightArr[j];
        j++;
        k++;
    }
}

// Function to perform Merge Sort
void mergeSort(int arr[], int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;  // Find the middle point

        // Sort the left half
        mergeSort(arr, left, mid);

        // Sort the right half
        mergeSort(arr, mid + 1, right);

        // Merge the two sorted halves
        merge(arr, left, mid, right);
    }
}

// Function to print the array
void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;
}

int main() {
    int arr[] = {64, 34, 25, 12, 22, 11, 90};  // Example array
    int n = sizeof(arr) / sizeof(arr[0]);

    cout << "Unsorted array: ";
    printArray(arr, n);

    mergeSort(arr, 0, n - 1);  // Call to Merge Sort function

    cout << "Sorted array (Decreasing order): ";
    printArray(arr, n);  // Print the sorted array

    return 0;
}
