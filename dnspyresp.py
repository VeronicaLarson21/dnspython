from dnspy import build_query, DNSQuestion, DNSHeader, response
from dataclasses import dataclass
import struct 
from io import BytesIO
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
    items = struct.unpack("!HHHHHH",reader.read(12))
    return DNSHeader(*items)

#The BytesIO object lets you keep a pointer at a position in a byte stream and read from and advance said pointer

#We now need to decode the domain name (writing out the broken example for learning)
def decode_name_broken(reader):
    parts = []
    while (length := reader.read(1)[0]) !=0:
        parts.append(reader.read(length))
    return b".".join(parts)
#not commenting bc it doesnt work

#This is the name decoder taking into account compression
def decode_name(reader):
    parts = []
    while(length := reader.read(1)[0]) != 0:
        if length & 0b1100_0000:
            parts.append(decode_compressed_name(length, reader))
            break
        else:
            parts.append(reader.read(length))
    return b".".join(parts)

#Handles compression decoding
def decode_compressed_name(length, reader):
    pointer_bytes = bytes([length
def parse_question(reader):
    name = decode_name_broken(reader)
    data = reader.read(4)
    type_, class_ = struct.unpack("!HH",data)
    return DNSQuestion(name, type_, class_)

def parse_record(reader):
    name = decode_name_broken(reader)
    #Type, class, TTL, and len = 10 bytes (2+2+4+2 bytes respectively)
    data = reader.read(10)
    # I=4byte int, so !HHIH
    type_,class_,ttl,data_len = struct.unpack("!HHIH",data)
    return DNSRecord(name, type_, class_, ttl, data)

#The reason why the other name decoding function fails is because DNS compresses the name which we have to take into account

























