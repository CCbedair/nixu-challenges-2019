from hashlib import sha1
import json
import codecs

metafile = json.load(open("meta.json"))
global flag
flag = ""
for meta in metafile:
    found = False
    for i in range(1, int(meta["range"])):
        nflag = flag + str(i)
        blobMeta = "blob "+str(len(nflag))+"\0"+nflag
        blob = sha1(blobMeta).hexdigest()
        treeMeta = "tree 36"+"\0"+"100644 flag.txt\0" + blob.decode('hex')
        tree = sha1(treeMeta).hexdigest()
        final = "tree "+tree+"\nparent "+meta['parent']+"\nauthor admin <admin@example.com> "+meta["time"]+"\ncommitter admin <admin@example.com> "+meta['time']+"\n\n"+meta["comment"]+"\n"
        commitMeta = "commit "+str(len(final))+"\0"+final
        commit = sha1(commitMeta).hexdigest()
        if commit == meta["hash"]:
            print meta["hash"]+ " " + str(i)
            flag += str(i)
            print flag
            found=True
            break
    if not found:
        print "Not Found: " + meta["hash"]
        print flag
        exit

stringFlag = hex(int(flag))[2:-1].decode("hex")
decodedFlag = codecs.encode(stringFlag, 'rot-13')

print decodedFlag

