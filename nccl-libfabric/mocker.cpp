#include <iostream>
#include <dlfcn.h>
#include <cassert>
#include <rdma/fabric.h>


// typedef int (*poll_cq_t)(struct ibv_cq *cq, int num_entries, struct ibv_wc *wc);
// static poll_cq_t native_poll_cq = NULL;

// extern "C" int poll_cq(struct ibv_cq *cq, int num_entries, struct ibv_wc *wc) {
//   std::cout << "Hello in poll_cq" << std::endl;
  
//   if (native_poll_cq == NULL) {
//     native_poll_cq = (poll_cq_t)dlsym(RTLD_NEXT, "poll_cq");
//   }
//   assert(native_poll_cq != NULL);

//   return native_poll_cq(cq, num_entries, wc);
// }


typedef int (*efa_cq_readfrom_t)(struct fid_cq *cq_fid, void *buf, size_t count, fi_addr_t *src_addr);
static efa_cq_readfrom_t native_efa_cq_readfrom = NULL;

extern "C" ssize_t efa_cq_readfrom(struct fid_cq *cq_fid, void *buf, size_t count, fi_addr_t *src_addr) {
  std::cout << "  Hello in efa_cq_readfrom" << std::endl;
  
  if (native_efa_cq_readfrom == NULL) {
    native_efa_cq_readfrom = (efa_cq_readfrom_t)dlsym(RTLD_NEXT, "efa_cq_readfrom");
  }
  assert(native_efa_cq_readfrom != NULL);

  return native_efa_cq_readfrom(cq_fid, buf, count, src_addr);
}
