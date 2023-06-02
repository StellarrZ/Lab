#include <iostream>
#include <algorithm>
#include <vector>

int n, r;


void comb_a() {
  std::vector<bool> v(n);
  std::fill(v.end() - r, v.end(), true);

  do {
    for (int i = 0; i < n; ++i) {
      if (v[i]) {
        std::cout << (i + 1) << " ";
      }
    }
    std::cout << "\n";
  } while (std::next_permutation(v.begin(), v.end()));
}


void comb_b() {
  std::vector<bool> v(n);
  std::fill(v.begin(), v.begin() + r, true);

  do {
    for (int i = 0; i < n; ++i) {
      if (v[i]) {
        std::cout << (i + 1) << " ";
      }
    }
    std::cout << "\n";
  } while (std::prev_permutation(v.begin(), v.end()));
}


int main() {
  std::cin >> n;
  std::cin >> r;

  comb_a();
  std::cout << "\n\n";
  comb_b();

  return 0;
}
