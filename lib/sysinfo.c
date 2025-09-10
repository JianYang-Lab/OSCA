// #define SYSINFO_SRC

// #include "sysinfo.h"

// #if defined __amd64__ || __x86_64__
// #if defined __linux__



// void
// get_sysinfo(SYSINFO_ptr data_in)
// {
//     data_in->cpu_arch = CPU_ARCH_X86;
//     data_in->os = OS_LINUX;
//     long phypz = sysconf(_SC_PHYS_PAGES);
//     long psize = sysconf(_SC_PAGE_SIZE);
//     data_in->mem_size_byte = phypz * psize;
//     unsigned int cpu, cpu_available;
//     cpu = sysconf(_SC_NPROCESSORS_CONF);
//     cpu_available = sysconf(_SC_NPROCESSORS_ONLN);
//     data_in->cpu_total = cpu;
//     data_in->cpu_available = cpu_available;

//     return;
// }


// /*borrowed from https://gist.github.com/ChisholmKyle/0cbedcd3e64132243a39*/
// /* recursive mkdir */
// int
// mkdir_p(const char *dir, const mode_t mode)
// {
//     char tmp[PATH_MAX_STRING_SIZE];
//     char *p = NULL;
//     struct stat sb;
//     size_t len;
    
//     /* copy path */
//     len = strnlen (dir, PATH_MAX_STRING_SIZE);
//     if (len == 0 || len == PATH_MAX_STRING_SIZE) {
//         return -1;
//     }
//     memcpy (tmp, dir, len);
//     tmp[len] = '\0';

//     /* remove trailing slash */
//     if(tmp[len - 1] == '/') {
//         tmp[len - 1] = '\0';
//     }

//     /* check if path exists and is a directory */
//     if (stat (tmp, &sb) == 0) {
//         if (S_ISDIR (sb.st_mode)) {
//             return 0;
//         }
//     }
    
//     /* recursive mkdir */
//     for(p = tmp + 1; *p; p++) {
//         if(*p == '/') {
//             *p = 0;
//             /* test path */
//             if (stat(tmp, &sb) != 0) {
//                 /* path does not exist - create directory */
//                 if (mkdir(tmp, mode) < 0) {
//                     return -1;
//                 }
//             } else if (!S_ISDIR(sb.st_mode)) {
//                 /* not a directory */
//                 return -1;
//             }
//             *p = '/';
//         }
//     }
//     /* test path */
//     if (stat(tmp, &sb) != 0) {
//         /* path does not exist - create directory */
//         if (mkdir(tmp, mode) < 0) {
//             return -1;
//         }
//     } else if (!S_ISDIR(sb.st_mode)) {
//         /* not a directory */
//         return -1;
//     }
//     return 0;
// }

// #endif
// #endif


// #ifdef SYSINFO_TEST
// #include <stdio.h>
// int
// main(void)
// {
//     SYSINFO data_in;
//     get_sysinfo(&data_in);
//     printf("%lu %u\n", data_in.mem_size_byte, data_in.cpu_total);
//     return 0;
// }
// #endif


#define SYSINFO_SRC

#include "sysinfo.h"

#if (defined(__x86_64__) || defined(__amd64__) || defined(__aarch64__) || defined(__arm64__))

    #if defined(__linux__)
        // -------- Linux --------
        #include <unistd.h>
        #include <sys/stat.h>
        #include <string.h>
        #include <limits.h>

        void get_sysinfo(SYSINFO_ptr data_in){
            data_in->cpu_arch = CPU_ARCH_X86;
            data_in->os = OS_LINUX;
            long phypz = sysconf(_SC_PHYS_PAGES);
            long psize = sysconf(_SC_PAGE_SIZE);
            data_in->mem_size_byte = phypz * psize;
            unsigned int cpu, cpu_available;
            cpu = sysconf(_SC_NPROCESSORS_CONF);
            cpu_available = sysconf(_SC_NPROCESSORS_ONLN);
            data_in->cpu_total = cpu;
            data_in->cpu_available = cpu_available;

            return;
        }

        int mkdir_p(const char *dir, const mode_t mode){
            char tmp[PATH_MAX_STRING_SIZE];
            char *p = NULL;
            struct stat sb;
            size_t len;
            
            /* copy path */
            len = strnlen (dir, PATH_MAX_STRING_SIZE);
            if (len == 0 || len == PATH_MAX_STRING_SIZE) {
                return -1;
            }
            memcpy (tmp, dir, len);
            tmp[len] = '\0';

            /* remove trailing slash */
            if(tmp[len - 1] == '/') {
                tmp[len - 1] = '\0';
            }

            /* check if path exists and is a directory */
            if (stat (tmp, &sb) == 0) {
                if (S_ISDIR (sb.st_mode)) {
                    return 0;
                }
            }
            
            /* recursive mkdir */
            for(p = tmp + 1; *p; p++) {
                if(*p == '/') {
                    *p = 0;
                    /* test path */
                    if (stat(tmp, &sb) != 0) {
                        /* path does not exist - create directory */
                        if (mkdir(tmp, mode) < 0) {
                            return -1;
                        }
                    } else if (!S_ISDIR(sb.st_mode)) {
                        /* not a directory */
                        return -1;
                    }
                    *p = '/';
                }
            }
            /* test path */
            if (stat(tmp, &sb) != 0) {
                /* path does not exist - create directory */
                if (mkdir(tmp, mode) < 0) {
                    return -1;
                }
            } else if (!S_ISDIR(sb.st_mode)) {
                /* not a directory */
                return -1;
            }
            return 0;
        }
    #elif defined(__APPLE__)
        // -------- macOS --------
        #include <sys/types.h>
        #include <sys/sysctl.h>
        #include <sys/stat.h>
        #include <string.h>
        #include <limits.h>
        #include <unistd.h>

        void get_sysinfo(SYSINFO_ptr data_in)
        {
            #if defined(__aarch64__) || defined(__arm64__)
                data_in->cpu_arch = CPU_ARCH_ARM64;
            #else
                data_in->cpu_arch = CPU_ARCH_X86;
            #endif

            data_in->os = OS_MACOS;

            // 获取内存大小
            int mib[2];
            int64_t physical_memory;
            size_t length = sizeof(physical_memory);

            mib[0] = CTL_HW;
            mib[1] = HW_MEMSIZE;

            sysctl(mib, 2, &physical_memory, &length, NULL, 0);
            data_in->mem_size_byte = (unsigned long)physical_memory;

            // 获取CPU总数
            int cpu_count;
            length = sizeof(cpu_count);
            mib[0] = CTL_HW;
            mib[1] = HW_NCPU;
            sysctl(mib, 2, &cpu_count, &length, NULL, 0);
            data_in->cpu_total = cpu_count;

            // macOS没有类似linux的cpu_available，这里直接赋cpu_total
            data_in->cpu_available = cpu_count;
        }

        int mkdir_p(const char *dir, const mode_t mode)
        {
            char tmp[PATH_MAX];
            char *p = NULL;
            struct stat sb;
            size_t len;

            len = strnlen(dir, PATH_MAX);
            if (len == 0 || len == PATH_MAX)
                return -1;
            memcpy(tmp, dir, len);
            tmp[len] = '\0';

            if (tmp[len - 1] == '/')
                tmp[len - 1] = '\0';

            if (stat(tmp, &sb) == 0)
            {
                if (S_ISDIR(sb.st_mode))
                    return 0;
            }

            for (p = tmp + 1; *p; p++)
            {
                if (*p == '/')
                {
                    *p = 0;
                    if (stat(tmp, &sb) != 0)
                    {
                        if (mkdir(tmp, mode) < 0)
                            return -1;
                    }
                    else if (!S_ISDIR(sb.st_mode))
                    {
                        return -1;
                    }
                    *p = '/';
                }
            }

            if (stat(tmp, &sb) != 0)
            {
                if (mkdir(tmp, mode) < 0)
                    return -1;
            }
            else if (!S_ISDIR(sb.st_mode))
            {
                return -1;
            }
            return 0;
        }


    #elif defined(_WIN32)
        // -------- Windows --------
       #include <windows.h>
        #include <direct.h>
        #include <string.h>

        void get_sysinfo(SYSINFO_ptr data_in)
        {
            data_in->cpu_arch = CPU_ARCH_X86;
            data_in->os = OS_WINDOWS;

            // 获取内存信息
            MEMORYSTATUSEX statex;
            statex.dwLength = sizeof(statex);
            GlobalMemoryStatusEx(&statex);
            data_in->mem_size_byte = (unsigned long long)statex.ullTotalPhys;

            // 获取CPU核心数
            SYSTEM_INFO sysinfo;
            GetSystemInfo(&sysinfo);
            data_in->cpu_total = sysinfo.dwNumberOfProcessors;
            data_in->cpu_available = sysinfo.dwNumberOfProcessors; // Windows没有区分在线和配置的处理器数量，赋相同值
        }

        int mkdir_p(const char *dir, const mode_t mode)
        {
            // Windows下_mode参数无用，递归创建目录
            char tmp[MAX_PATH];
            size_t len = strlen(dir);
            if (len == 0 || len > MAX_PATH)
                return -1;

            strcpy(tmp, dir);

            // 去掉尾部斜杠
            if (tmp[len - 1] == '\\' || tmp[len - 1] == '/')
                tmp[len - 1] = '\0';

            // 递归创建目录
            for (char *p = tmp + 1; *p; p++)
            {
                if (*p == '\\' || *p == '/')
                {
                    *p = '\0';
                    if (_access(tmp, 0) != 0)
                    {
                        if (_mkdir(tmp) != 0)
                            return -1;
                    }
                    *p = '\\';
                }
            }

            if (_access(tmp, 0) != 0)
            {
                if (_mkdir(tmp) != 0)
                    return -1;
            }
            return 0;
        }
    #else
        #error Unsupported platform
    #endif

#else
    #error Unsupported CPU architecture
#endif

#ifdef SYSINFO_TEST
#include <stdio.h>
int main(void)
{
    SYSINFO data_in;
    get_sysinfo(&data_in);
    printf("Memory size: %lu bytes\n", data_in.mem_size_byte);
    printf("CPU total: %u\n", data_in.cpu_total);
    printf("CPU available: %u\n", data_in.cpu_available);
    return 0;
}
#endif