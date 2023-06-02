#include <iostream>
#include <cmath>
#include <algorithm>
#include <cassert>
#include <vector>
#include <queue>


const int ah_max_num = 1024;
const int max_nodes_per_partition = ah_max_num / 2;

const int world_size = 0;


inline int get_num_partitions(const int cluster_size) {
  int ret;
  if (cluster_size <= 1) {
    ret = -1;
  } else if (cluster_size <= ah_max_num) {
    ret = 2;
  } else {
    ret = (int)std::lrint(ceil(2 * cluster_size / (float)ah_max_num));
  }
  return ret;
}


inline int round_full(const int num_partitions) {
  return num_partitions * (num_partitions - 1) / 2;
}

inline int round_ring(const int num_partitions) {
  return num_partitions == 2 ? 1 : num_partitions;
}



int main(int argc, char** argv) {
  int num_partitions = -1;

  for (int i = 1024; i < 1E4; i++) {
    num_partitions = get_num_partitions(i);
    std::cout << "size  " << i << "  partitions  " << num_partitions << std::endl;
    // assert(num_partitions * 2 <= ah_max_num);
  
    std::queue<int> cur_groups;
    cur_groups.push(0);

    // Full mesh
    for (int round = 0; round < round_full(num_partitions); round++) {
      cur_groups.push();

      // create ah if round 0 else delete ah

      // create ah

      // checks
    }

    // Ring mesh
    for (int round = 0; round < round_full(num_partitions); round++) {
      cur_groups.push((round + 1) % round_full(num_partitions));
      
      // create ah if round 0 else delete ah

      // create ah

      // checks
    }

  }

  

  return 0;
}