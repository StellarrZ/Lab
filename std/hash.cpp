#include <functional>
#include <unordered_map>
#include <vector>
#include <cstdio>


int main() {
  std::unordered_map<size_t, std::vector<int>> m;
  for (int i = 0; i < 5; i++) {
    m.emplace(std::hash<int>{}(i % 2), std::vector<int>());
    m.at(std::hash<int>{}(i % 2)).push_back(i);
  }

  for (auto pair : m) {
    for (auto val : pair.second) {
      printf("%ld  %d\n", pair.first, val);
    }
  }

  return 0;
}