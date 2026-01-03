#DNS queries have 2 parts, header and a question
#We need a class for both, a way to convert both object to bytes, and a function to build the query

from dataclasses import dataclass
import dataclasses
import struct
import random
import socket

#DNSHeader class
#I will update this for style conventions later (I have no clue what they are for python lol)
#Inputs: id: int, query ID, flags: int,on tin, num_questions: int, tin, num_answers: int, tin, num_authorities: int, tin, num_additionals: int, tin
# The "num" inputs represent how many records you should expect of each type
@dataclass
class DNSHeader:
    id: int
    flags: int
    num_questions: int = 0
    num_answers: int = 0
    num_authorities: int = 0
    num_additionals: int = 0

#DNSQuestion class
#See above re style conventions
#Inputs: name: bytes, domain name, type: int, not sure, class: int, not sure

@dataclass
class DNSQuestion:
    name: bytes
    type_: int
    class_: int

#Convert header to byte string
def header_to_bytes(header):
    fields = dataclasses.astuple(header)
    #6 H's for 6 fields
    #H = 2 byte integer 
    #so struct.pack("!HHHHHH",*fields) means that we want to format fields (6 ints) as 6 2 byte integers
    #! at the beginning signals to use big endian byte order (default for networking)
    return struct.pack("!HHHHHH", *fields)

# Convert header to byte string
def question_to_bytes(question):
    return question.name+struct.pack("!HH",question.type_,question.class_)

#To encode a domain name as a byte string for the question, we create a function to handle it
#this returns a byte string representing each part beginning with its length (ex google and com, or twitch and tv)
def encode_dns_name(domain_name):
    #creates empty byte string
    encoded = b""
    #Split the domain name into parts and then append number of bytes in part (len converted) and part to our empty byte string
    for part in domain_name.encode("ascii").split(b"."):
        encoded +=bytes([len(part)])+part

    #Return the encoded byte string with a zero byte at the end
    return encoded+ b"\x00"

#Set up for build_query function
random.seed(1)

#Encoding of type A (host address)
TYPE_A = 1

#Encoding of class IN (internet)
CLASS_IN = 1

#The function to build the query, with the inputs being domain name and dns record type
def build_query(domain_name, record_type):
    #Encode the domain name as a byte string
    name = encode_dns_name(domain_name)
    #Pick a random ID for the query
    id = random.randint(0,65535)
    #Sets the flag for recursion desired ( 9th bit from the right in the flags field)
    # 1 << 8 creates a value of 1 with 8 zeros behind it, accurately encoding the flag
    RECURSION_DESIRED = 1 << 8
    #Create header and question, then concatenate them
    header = DNSHeader(id=id, num_questions=1,flags=RECURSION_DESIRED)
    question = DNSQuestion(name=name, type_=record_type, class_=CLASS_IN)
    return header_to_bytes(header)+question_to_bytes(question)

#Testing sending our query to 8.8.8.8:53 (google dns resolver)
query = build_query("www.example.com",1)

#Creating a UDP socket
# socket.AF_INET = connecting to internet
# socket.SOCK_DGRAM = UDP

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Send the query to the resolver at port 53 (dns port)

sock.sendto(query, ("8.8.8.8",53))

response, _ = sock.recvfrom(1024)




































