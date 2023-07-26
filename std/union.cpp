#include <iostream>

typedef enum {
  succ,
  fail,
} A;

typedef unsigned B;

class C {
public:
  union {
    A code_a;
    B code_b;
  };

  C() = default;
  ~C() = default;
};


int main() {
  C cc;

  cc.code_b = 2;
  std::cout << cc.code_a << std::endl;

  return 0;
}