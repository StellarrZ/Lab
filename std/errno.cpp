#include <iostream>
#include <cstring>
#include <cerrno>
#include <string>

#define INCLUDE(msg, x) (msg += std::string(#x) + std::string(" is ") + std::to_string(x) + std::string("; "));


int SuccessFn() {
  return 0;
}

int FlawedFn() {
  errno = 222;
  return 0;
}

int main() {
  int* arr = new int[0];
  printf("%p\n", arr);
  printf("%d\n", arr[0]);

  printf("\n%d\n", errno);
  errno = 111;
  printf("%d\n\n", errno);

  auto ret = SuccessFn();
  printf("%d\n\n", errno);

  errno = 0;
  ret = FlawedFn();
  printf("%d\n\n", errno);

  std::cout << std::strerror(EPERM) << std::endl;
  std::cout << (int)EPERM << std::endl;

  std::cout << std::strerror(ENOSYS) << std::endl;
  std::cout << (int)ENOSYS << std::endl;

  std::cout << std::strerror(ENOMEM) << std::endl;
  std::cout << (int)ENOMEM << std::endl;


  std::string s;
  int foo = 5, bar = 10;
  INCLUDE(s, foo - bar);
  std::cout << s << std::endl;

  return 0;
}