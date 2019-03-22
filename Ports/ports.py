from scapy.all import rdpcap, TCP
from base64 import decodestring
from codecs import encode

pkts = rdpcap('ports.pcap')
print encode(decodestring(''.join([ chr(p[TCP].dport) for p in pkts])), 'rot_13')
