# vce-1.0-fw-convertor
VCE 1.0 firmware convertor from radeon to amdgpu driver

This script creates a VCE 1.0 firmware using the new format for amdgpu, which simply adds a header with some information.
This script is based on Piotr Redlewski's work, available at https://gist.github.com/anonymous/6d974a970340f7f64b6fcc4f95267e43.

Structure of the header is as follow:

struct common_firmware_header {
    uint32_t size_bytes; /* size of the entire header with full offset+image(s) in bytes: 256+original firmware's length */
    uint32_t header_size_bytes; /* size of just the header's structure in bytes: 32 */
    uint16_t header_version_major; /* header version: 1 */
    uint16_t header_version_minor; /* header version: 0 */
    uint16_t ip_version_major; /* IP version: 1 */
    uint16_t ip_version_minor; /* IP version: 0 */
    uint32_t ucode_version;
    uint32_t ucode_size_bytes; /* size of ucode in bytes: original firmware's length */
    uint32_t ucode_array_offset_bytes; /* payload offset from the start of the header: 256 */
    uint32_t crc32;  /* crc32 checksum of the payload */
};

However, even with the added header, once the VCE code will be completed, the resulting firmware may not be enough and an official firmware from AMD may be needed.
