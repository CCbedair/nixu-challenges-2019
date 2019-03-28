# The steps for solving the Stowaway challenge 

1. First of all, we opened the available files and understood the problem. ![The picture of this step](step1.jpg)
2. The file is base64 encoding configuration. We need to decode from base 64 to human-readable file (.nxa files). ![The picture of this step](step2.jpg)
3. We looked at the binary of .nxa files using xcd. The header of files states that the file is NXA. ![The picture of this step](step3.jpg)
4. We take a look inside the binary files. We found out the beginning and end of two certificate files. 
5. Let's extract the certificate files. ![The picture of this step](step5.jpg)
6. We checked the certificates and found out that they are not valid, since the date already expired. ![The picture of this step](step6.jpg) ![The picture of this step](step6.1.jpg)
7. After a long tryouts and analyzing the gile structure, we see the common structure of packing and unpacking, where 1 byte before the title specifies the content and 1 byte specifies the size of string. ![The picture of this step](Unknown-2)
8. We found out that the IoT device takes the first certificate found, therefore, if we add and change the name of certificate that needs to match with manifest with checksums. We rename the certificate name to coder.cert instead of john.cert. 
9. Now the IoT device can get the certificate and update itself. ![The picture of this step](Unknown)

# The flag 
NIXU{th3_mAnIfEsT_0nly_l1sts_wh4t_SHOULD_bE_iNCLud3d}
