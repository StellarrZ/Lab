// #include <sys/types.h>
// #include <ifaddrs.h>
#include <iostream>
#include <string>
#include <cstring>


// #define _GNU_SOURCE     /* To get defns of NI_MAXSERV and NI_MAXHOST */
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netdb.h>
#include <ifaddrs.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <linux/if_link.h>


int main() {
  int ret;
  struct ifaddrs* ifaddr;
  ret = getifaddrs(&ifaddr);
  if (ret) {
    printf("Error %s\n", gai_strerror(ret));
    exit(1);
  }

  int family, err;
  char host[NI_MAXHOST];
  for (struct ifaddrs *ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
    if (ifa->ifa_addr == NULL) continue;

    family = ifa->ifa_addr->sa_family;
    if (family != AF_INET) continue;

    if (strncmp(ifa->ifa_name, "lo", 2) == 0 ||
        strncmp(ifa->ifa_name, "docker", 6) == 0) {
      continue;
    }

    ret = getnameinfo(ifa->ifa_addr,
                      sizeof(struct sockaddr_in),
                      host, NI_MAXHOST,
                      NULL, 0, NI_NUMERICHOST);
    if (ret != 0) {
        printf("Error %s\n", gai_strerror(ret));
        exit(1);
    }

    printf("%s\n", host);
  }

  return 0;
}



// int main() {
//   struct ifaddrs* ifaddr;
//   if (getifaddrs(&ifaddr)) {
//     std::cerr << "Error" << std::endl;
//   }

//   int family, s;
//   char host[NI_MAXHOST];
//   for (struct ifaddrs *ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
//     if (ifa->ifa_addr == NULL)
//         continue;
//     // else {
//     //   // std::string s(ifa->ifa_addr->sa_data);
//     //   // std::cout << s << std::endl;
//     //   // std::cout << std::string(ifa->ifa_name) << std::endl;
//     //   if (std::string(ifa->ifa_name) == "eth0") {
//     //     std::cout << "HERE" << std::endl;
//     //   }
//     // }

//     family = ifa->ifa_addr->sa_family;

//     if (family != AF_INET) continue;

//     /* Display interface name and family (including symbolic
//       form of the latter for the common families). */

//     printf("%-8s %s (%d)\n",
//           ifa->ifa_name,
//           (family == AF_PACKET) ? "AF_PACKET" :
//           (family == AF_INET) ? "AF_INET" :
//           (family == AF_INET6) ? "AF_INET6" : "???",
//           family);

//     /* For an AF_INET* interface address, display the address. */

//     if (family == AF_INET || family == AF_INET6) {
//         s = getnameinfo(ifa->ifa_addr,
//                 (family == AF_INET) ? sizeof(struct sockaddr_in) :
//                                       sizeof(struct sockaddr_in6),
//                 host, NI_MAXHOST,
//                 NULL, 0, NI_NUMERICHOST);
//         if (s != 0) {
//             printf("getnameinfo() failed: %s\n", gai_strerror(s));
//             exit(EXIT_FAILURE);
//         }

//         printf("\t\taddress: <%s>\n", host);

//     } else if (family == AF_PACKET && ifa->ifa_data != NULL) {
//         struct rtnl_link_stats *stats = (struct rtnl_link_stats *)ifa->ifa_data;

//         printf("\t\ttx_packets = %10u; rx_packets = %10u\n"
//               "\t\ttx_bytes   = %10u; rx_bytes   = %10u\n",
//               stats->tx_packets, stats->rx_packets,
//               stats->tx_bytes, stats->rx_bytes);
//     }
// }

//   return 0;
// }
