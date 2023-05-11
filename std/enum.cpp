#include <iostream>

enum status {
  A,
  B,
  C,
};

int main() {
  int a = A;
  int b = B;
  int c = C;
  int z = A - 1;

  std::cout << a << std::endl;
  std::cout << b << std::endl;
  std::cout << c << std::endl;

  std::cout << z << std::endl;

  // // Not allowed
  // status q = A - 1;

  return 0;
}