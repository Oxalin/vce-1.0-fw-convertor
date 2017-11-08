#!/usr/bin/python -utt
  
import sys
import struct

with open(sys.argv[1], mode='rb') as file:
        fileContent = file.read()

with open(sys.argv[2], mode='wb') as output:
        output.write(struct.pack('IIHHHHIIII', len(fileContent) + 512, 32, 1, 0, 4, 0, 0, len(fileContent), 256, 0))
        output.write(bytearray(512-32))
        output.write(fileContent)

#struct common_firmware_header {
#        uint32_t size_bytes; /* size of the entire header+image(s) in bytes */
#        uint32_t header_size_bytes; /* size of just the header in bytes */
#        uint16_t header_version_major; /* header version */
#        uint16_t header_version_minor; /* header version */
#        uint16_t ip_version_major; /* IP version */
#        uint16_t ip_version_minor; /* IP version */
#        uint32_t ucode_version;
#        uint32_t ucode_size_bytes; /* size of ucode in bytes */
#        uint32_t ucode_array_offset_bytes; /* payload offset from the start of the header */
#        uint32_t crc32;  /* crc32 checksum of the payload */
#};   
