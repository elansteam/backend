#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<int> sp(n);

    for (int i = 0; i < n; ++i) {
        cin >> sp[i];
    }

    for (int i = 0; i < n; ++i) {
        cout << sp[i] << " ";
    }

    return 0;
}