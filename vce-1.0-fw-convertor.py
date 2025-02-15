#!/usr/bin/python -utt

# Create a VCE 1.0 firmware using the new format for amdgpu, which simply adds a header with some information.
# This work is based on Piotr Redlewski's work.
#
# Structure of the header is as follow:
#
#struct common_firmware_header {
#        uint32_t size_bytes; /* size of the entire header with full offset (common firmware header)+image(s) in bytes: 256 + original firmware's length */
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

import binascii
import re
import struct
import sys

def payload_crc32_checksum(payload_file):
    crc32_checksum = 0
    payload = open(payload_file, mode='rb')
    for eachLine in payload:
        crc32_checksum = binascii.crc32(eachLine, crc32_checksum)
    payload.close
    return (crc32_checksum & 0xFFFFFFFF)

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
crc32 = payload_crc32_checksum(sys.argv[1])

# Find ucode version from actual firmware
fw_version = "[ATI LIB=VCEFW,"  # 15 Bytes / max 25 bytes
fb_version = "[ATI LIB=VCEFWSTATS," # 20 Bytes / max 32 bytes
bfw_version = bytes(b"[ATI LIB=VCEFW,")
bfb_version = bytes(b"[ATI LIB=VCEFWSTATS,")

index = fileContent.find(bfw_version)
if (index == 0) :
    print("fw_version not found")
    exit

# Search for version string
# Extract version string with a maximum length of 25 bytes
# Then split this array at each "." and the end character "]"
ucodeString = (fileContent[index+len(bfw_version) : index+25]).decode('utf-8')
subUcodeString = re.split("]", ucodeString)[0]
splittedUCodeString = re.split("\\.", subUcodeString)

if len(splittedUCodeString) != 3:
    print("fw_version format did not match")
    exit

version_major = int(splittedUCodeString[0])
version_minor = int(splittedUCodeString[1])
binary_id = int(splittedUCodeString[2])
print("uCode version found: {}.{}.{}".format(version_major, version_minor, binary_id))

# ucode_version's format is 32 bits as version_major 12 bits | version_minor 12 bits | binary_id 8 bits
ucode_version = ((version_major << 20) | (version_minor << 8) | (binary_id << 0))

# # search for feedback version
index = fileContent.find(bfb_version)
if (index == 0) :
    print("fb_version not found")
    exit

# Search for feedback string, even though it is not used in the CFH
# Extract version string with a maximum length of 32 bytes
# Then split this array at each "." and the end character "]"
feedbackString = (fileContent[index+len(bfb_version) : index+32]).decode('utf-8')
subFeedbackString= re.split("]", feedbackString)

if len(subFeedbackString) != 2:
    print("fb_version format did not match")
    exit

version_feedback = int(subFeedbackString[0])
print("Feedback version found: {}".format(version_feedback))


cfh_struct_format = "IIHHHHIIII"

print ("Header's properties to be added to original VCE firmware [{}]".format(sys.argv[1]))
print ("Total size of new firmware [{}]: {}B [uint32]".format(sys.argv[2], firmware_size_bytes))
print ("Header's size: {}B [uint32]".format(header_size_bytes))
print ("Header's version: {}.{} [2*uint16]]".format(header_version_major, header_version_minor))
print ("IP [VCE] version: {}.{} [2*uint16]".format(ip_version_major, ip_version_minor))
print ("uCode version: {} [uint32]".format(ucode_version))
print ("uCode's size: {}B [uint32]".format(ucode_size_bytes))
print ("uCode's offset: {}B [uint32]".format(ucode_array_offset_bytes))
print ("uCode's CRC32 checksum: {} [uint32]".format(crc32))

with open(sys.argv[2], mode='wb') as output:
        output.write(struct.pack(cfh_struct_format,
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
