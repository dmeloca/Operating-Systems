#include <iostream>
#include <vector>
#include <thread>

using namespace std;

const int MAX_DEPTH_RECURSION = 3;

int partition(vector<int>& arr, int left, int right) {
    int pivot = arr[right];
    int i = left - 1;

    for (int j = left; j < right; ++j) {
        if (arr[j] < pivot) {
            ++i;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[right]);
    return i + 1;
}

void quickSort(vector<int>& arr, int left, int right, int depth = 0) {
    if (left >= right)
        return;

    int pivotIndex = partition(arr, left, right);

    if (depth < MAX_DEPTH_RECURSION) {
        thread t1(quickSort, ref(arr), left, pivotIndex - 1, depth + 1);
        thread t2(quickSort, ref(arr), pivotIndex + 1, right, depth + 1);
        t1.join();
        t2.join();
    } else {
        quickSort(arr, left, pivotIndex - 1, depth + 1);
        quickSort(arr, pivotIndex + 1, right, depth + 1);
    }
}

int main() {
    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; i++)
        cin >> arr[i];

    quickSort(arr, 0, n - 1);

    for (int i = 0; i < n; i++)
        cout << arr[i] << " ";
    cout << endl;

    return 0;
}
