#include <map>
#include <memory>


class A {
public:
  A() = default;
  ~A() = default;
};


int main() {
  std::map<size_t, std::unique_ptr<A>> m;

  auto& ptr = m[3];
  printf("%p\n", ptr.get());

  auto a = std::make_unique<A>();
  ptr = std::move(a);
  printf("%p\n", ptr.get());
  
  printf("%p\n", m[3].get());

  ptr.reset();
  printf("%p\n", m[3].get());

  printf("%p\n", m[6].get());
  
  std::map<size_t, char> m2;
  printf("%u\n", m2[6]);

  return 0;
}