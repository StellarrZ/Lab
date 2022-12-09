#include <cstdio>

int main(int argc, char** argv) {
  void* p0 = (void*)0x8000;
  size_t mask = 0x0007;

  float a[10];
  printf("%p  %p\n", &a[0], &a[1]);

  for (size_t p = (size_t)p0; p < 0x8010; p++) {
    printf("%p  ", (void*)p);
    if (p & mask) {
      printf("IF\n");
    } else {
      printf("ELSE\n");
    }
  }

  return 0;
}