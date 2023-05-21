#include <iostream>
#include <cstdio>
#include <cuda_runtime.h>
#include <hwloc.h>


int main() {
  int num_gpu;
  cudaGetDeviceCount(&num_gpu);

  cudaDeviceProp property;
  std::cout << "     pciDomainID, pciBusID, pciDeviceID\n" << std::endl;
  for (int i = 0; i < num_gpu; i++) {
    cudaGetDeviceProperties(&property, i);
    printf("[%d]  %d, %d, %d\n", i, property.pciDomainID, property.pciBusID, property.pciDeviceID);
  }

  std::cout << std::endl;

  hwloc_topology_t topology;
  hwloc_topology_init(&topology);
  // we need to handle hwloc1.x and hwloc2.x differently
#if HWLOC_API_VERSION < 0x20000
  hwloc_topology_set_flags(topology, HWLOC_TOPOLOGY_FLAG_IO_DEVICES);
#else
  hwloc_topology_set_io_types_filter(topology, HWLOC_TYPE_FILTER_KEEP_ALL);
#endif
  hwloc_topology_load(topology);

  // Nvidia PCI vender ID 
  // https://devicehunt.com/view/type/pci/vendor/10DE/device/20B0
  unsigned short nv_vender_id = 0x10DE;  // 4318
  hwloc_obj_t gpu_obj = nullptr;
  while ((gpu_obj = hwloc_get_next_pcidev(topology, gpu_obj)) != nullptr) {
    if (gpu_obj->attr->pcidev.vendor_id == nv_vender_id) {
      printf("     %hu, %hu, %hu,\n", 
            gpu_obj->attr->pcidev.domain, gpu_obj->attr->pcidev.bus, gpu_obj->attr->pcidev.dev);
    }
  }

  return 0;
}