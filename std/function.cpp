#include <iostream>
#include <functional>
// #include <utility>
#include <type_traits>


template <class> struct Decorator;

template <class Fn, class... Args>
struct Decorator<Fn(Args ...)>
{
  using Fn_t = std::function<Fn(Args ...)>;
  Decorator(Fn_t f) : f_(f) {}

  Fn operator()(Args ... args) {
    // if constexpr(std::is_same<typename std::result_of<Fn_t(Args ...)>::type, void>::value) {  // c++11
    if constexpr(std::is_same<typename std::invoke_result<Fn_t, Args...>::type, void>::value) {  // c++17
      f_(args...);
      std::cout << "Decorated the void function." << std::endl;
    } else {
      auto ret = f_(args...);
      std::cout << "Decorated the non-void function." << std::endl;
      return ret;
    }
  }

  Fn_t f_;
};


template<class Fn, class... Args>
std::function<Fn(Args...)> makeDecorator(Fn (*f)(Args ...)) {
  return Decorator<Fn(Args...)>(f);
}


int foo() {
  std::cout << "foo()" << std::endl;
  return 0;
}

void bar() {
  std::cout << "bar()" << std::endl;
}

inline int baz() {
  std::cout << "baz()" << std::endl;
  return 1;
}

int main() {
  auto d_foo = makeDecorator(foo);
  d_foo();
  auto d_bar = makeDecorator(bar);
  d_bar();
  auto d_baz = makeDecorator(baz);
  d_baz();
  
  return 0;
}