# My solution for "Port" challenge.

The steps:
1. First of all, we open the provided file ports.pcap in wireshark;
2. We saw the bunch of TCP port numbers;
3. The suspicious part is lack of stream;
4. Then we look at the destination of port and found an interesting pattern;
5. In order to solve this challenge I created the script porty.py, that you can see in this directory.

# The flag
The flag for this challenge is NIXU{symbols_and_numbers_are_fun_to_play_with}
