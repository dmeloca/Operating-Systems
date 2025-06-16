#include <iostream>
#include <vector>
#include <thread>
#include <algorithm>

const int MAX_DEPTH_RECURSION = 3;
using namespace std;

void merge(vector<int>& arr, int left, int mid, int right) {
    vector<int> temp(right - left + 1);
    int i = left, j = mid + 1, k = 0;

    while (i <= mid && j <= right)
        temp[k++] = (arr[i] < arr[j]) ? arr[i++] : arr[j++];

    while (i <= mid)
        temp[k++] = arr[i++];
    while (j <= right)
        temp[k++] = arr[j++];

    copy(temp.begin(), temp.end(), arr.begin() + left);
}

void merge_sort(vector<int>& arr, int left, int right, int depth = 0) {
    if (left >= right)
        return;

    int mid = left + (right - left) / 2;

    if (depth < MAX_DEPTH_RECURSION) {
        thread t1(merge_sort, ref(arr), left, mid, depth + 1);
        thread t2(merge_sort, ref(arr), mid + 1, right, depth + 1);
        t1.join();
        t2.join();
    } else {
        merge_sort(arr, left, mid, depth + 1);
        merge_sort(arr, mid + 1, right, depth + 1);
    }

    merge(arr, left, mid, right);
}

int main() {
    int n;
    cin >> n;

    vector<int> arr(n);
    for (int i = 0; i < n; i++)
        cin >> arr[i];

    merge_sort(arr, 0, n - 1);

    for (int i = 0; i < n; i++)
        cout << arr[i] << " ";
    cout << "\n";

    return 0;
}
