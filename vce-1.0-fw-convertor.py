#!/usr/bin/python -utt

# Create a VCE 1.0 firmware using the new format for amdgpu, which simply adds a header with some information.
# This work is based on Piotr Redlewski's work.
#
# Structure of the header is as follow:
#
#struct common_firmware_header {
#        uint32_t size_bytes; /* size of the entire header with full offset+image(s) in bytes: 256+original firmware's length */
#        uint32_t header_size_bytes; /* size of just the header's structure in bytes: 32 */
#        uint16_t header_version_major; /* header version: 1 */
#        uint16_t header_version_minor; /* header version: 0 */
#        uint16_t ip_version_major; /* IP version: 1 */
#        uint16_t ip_version_minor; /* IP version: 0 */
#        uint32_t ucode_version;
#        uint32_t ucode_size_bytes; /* size of ucode in bytes: original firmware's length */
#        uint32_t ucode_array_offset_bytes; /* payload offset from the start of the header: 256 */
#        uint32_t crc32;  /* crc32 checksum of the payload */
#};

import sys
import struct

with open(sys.argv[1], mode='rb') as file:
        fileContent = file.read()

header_size_bytes = 32
header_version_major = 1
header_version_minor = 0
ip_version_major = 1
ip_version_minor = 0
ucode_version = 1
ucode_size_bytes = len(fileContent)
ucode_array_offset_bytes = 256
firmware_size_bytes = ucode_size_bytes + ucode_array_offset_bytes
crc32 = 0

with open(sys.argv[2], mode='wb') as output:
        output.write(struct.pack('IIHHHHIIII', 
                                 firmware_size_bytes, 
                                 header_size_bytes, 
                                 header_version_major, 
                                 header_version_minor, 
                                 ip_version_major, 
                                 ip_version_minor, 
                                 ucode_version, 
                                 ucode_size_bytes, 
                                 ucode_array_offset_bytes, 
                                 crc32))
        output.write(bytearray(ucode_array_offset_bytes - header_size_bytes))
        output.write(fileContent)
        