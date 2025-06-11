#include <iostream>
#include <vector>

float average(int n, std::vector<int> v) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += v[i];
    }
    return sum / n;
}

int get_max(std::vector<int> v) {
    int max = v[0];
    for (int& x: v) {
       if (x > max) {
            max = x;
        }
    }
    return max;
}

int get_min(std::vector<int> v) {
    int min = v[0];
    for (int& x: v) {
        if (x < min) {
            min = x;
        }
    }
    return min;
}

int main() {
    int n = 0;
    std::cin >> n;
    std::vector<int> arr(n);
    for (int& x: arr) {
        std::cin >> x;
    }
    std::cout << "The avarage value is: " << average(n, arr) << std::endl;
    std::cout << "The minimum value is: " << get_min(arr) << std::endl;
    std::cout << "The maximum value is: " << get_max(arr) << std::endl;

    return 0;
}
