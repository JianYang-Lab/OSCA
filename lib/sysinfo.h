// #ifndef SYSINFO_HEAD
// #define SYSINFO_HEAD

// #if !defined SYSINFO_SRC
// #define SYSINFO_EXTERN extern
// #else
// #define SYSINFO_EXTERN
// #endif

// #ifdef __linux__

// #include <stdint.h>
// #include <string.h>
// #include <sys/stat.h>
// #include <sys/types.h>
// #include <unistd.h>

// #define CPU_ARCH_X86 1
// #define CPU_ARCH_ARM 2
// #define CPU_ARCH_RISCV 3
// #define OS_LINUX 1
// #define OS_MACOS 2
// #define OS_WINDOWS 3
// #define PATH_MAX_STRING_SIZE 1024

// typedef struct sysinfo {
//     char cpu_arch;
//     char os;
//     uint64_t mem_size_byte;
//     uint32_t cpu_total;
//     uint32_t cpu_available; 
// } SYSINFO, *SYSINFO_ptr;

// #ifdef __cplusplus
// extern "C" {
// #endif

// void get_sysinfo(SYSINFO_ptr sysinfo_data);

// int mkdir_p(const char *dir, const mode_t mode);

// #ifdef __cplusplus
// }
// #endif

// #endif

// #endif

#ifndef SYSINFO_HEAD
#define SYSINFO_HEAD

#if !defined SYSINFO_SRC
#define SYSINFO_EXTERN extern
#else
#define SYSINFO_EXTERN
#endif

// 平台无关的头文件
#include <stdint.h>

#if defined(__linux__) || defined(__APPLE__)
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#elif defined(_WIN32)
#include <direct.h>
#endif

// 支持的CPU架构
#define CPU_ARCH_X86    1
#define CPU_ARCH_ARM    2
#define CPU_ARCH_ARM64  3
#define CPU_ARCH_RISCV  4

// 支持的操作系统
#define OS_LINUX    1
#define OS_MACOS    2
#define OS_WINDOWS  3

// 最大路径字符串长度
#define PATH_MAX_STRING_SIZE 1024

// 系统信息结构体
typedef struct sysinfo {
    char cpu_arch;              // 架构代号
    char os;                    // 操作系统代号
    uint64_t mem_size_byte;     // 内存总字节数
    uint32_t cpu_total;         // 总CPU核数
    uint32_t cpu_available;     // 可用CPU核数
} SYSINFO, *SYSINFO_ptr;

#ifdef __cplusplus
extern "C" {
#endif

// 获取系统信息
void get_sysinfo(SYSINFO_ptr sysinfo_data);

// 递归创建目录
int mkdir_p(const char *dir, const mode_t mode);

#ifdef __cplusplus
}
#endif

#endif // SYSINFO_HEAD