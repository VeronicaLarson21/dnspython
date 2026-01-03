from dnspy import build_query, DNSQuestion, DNSHeader
from dataclasses import dataclass
import struct 

#The response is going to be a DNS Record, which we need to define a class for
#Inputs: name: byte string, domain name, type: int, unsure, class: int, allways 1 (internet), ttl: int, how long to cache query, data: byte string, the records content (ip address)
@dataclass
class DNSRecord:
    name: bytes
    type_: int
    class_: int
    ttl: int
    data: bytes

#To parse the header we basically reverse the function we created to encode it as a byte
def parse_header(reader):




























