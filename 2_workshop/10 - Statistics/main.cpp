#include <iostream>
#include <vector>
#include <thread>

void average(int n, const std::vector<int>& v) {
    int sum = 0;
    for (int x : v) {
        sum += x;
    }
    std::cout << "The average value is: " << sum / n << std::endl;
}

void get_max(const std::vector<int>& v) {
    int max = v[0];
    for (int x : v) {
        if (x > max) {
            max = x;
        }
    }
    std::cout << "The maximum value is: " << max << std::endl;
}

void get_min(const std::vector<int>& v) {
    int min = v[0];
    for (int x : v) {
        if (x < min) {
            min = x;
        }
    }
    std::cout << "The minimum value is: " << min << std::endl;
}

int main() {
    int n;
    std::cin >> n;
    std::vector<int> arr(n);
    for (int& x : arr) {
        std::cin >> x;
    }

    std::thread t1(average, n, std::ref(arr));
    std::thread t3(get_min, std::ref(arr));
    std::thread t2(get_max, std::ref(arr));

    t1.join();
    t2.join();
    t3.join();

    return 0;
}
