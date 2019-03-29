import binascii
INSTRUCTIONS = ["HALT","ADD","SUB","MUL","DIV","XOR","MOD","AND","OR","INV","PUSHI","PUSHF","PUSHSTR","PUSHSY","PUSHSYRAW","PUSHTRUE","PUSHFALSE","PUSHUNIT","PUSHCLOSURE","PUSHCONT","QUOTED","POP","CALL","TAILCALL","RET","JT","JF","JMP","STORE","STORETOP","EQ","NEQ","GT","GE","LT","LE","NOT","DECLARE","PRINT","LIST","HEAD","TAIL","LISTCAT","EVAL","DUMP","NEWENV","DEPARTENV"]
SPECIAL_INSTRUCTIONS = ["PUSHI","PUSHF","PUSHSTR","PUSHSY","STORE","STORETOP","PUSHCLOSURE","JT","JF","JMP","DECLARE","LIST","PUSHSYRAW","QUOTED","PUSHCONT"]
MAGIC = "LISBY001"
C = 0
flag  = ""
with open("lisby1", "rb") as f:
    dump = f.read()


def read_buffer(n):
    global C
    C += n
    return dump[C-n:C]


def int_from_bin(bin):
    hexbin = binascii.b2a_hex(bin)
    b = [hexbin[i:i+2] for i in range(0, len(hexbin), 2)][::-1]
    return int(''.join(b), 16)


def read_table():
    size = int_from_bin(read_buffer(8))
    strings = []
    for i in range(size):
        strings.append(read_buffer(int_from_bin(read_buffer(8))))
    return strings


def read_tapes():
    number = int_from_bin(read_buffer(8))
    tapes = []
    for i in range(number):
        tape = []
        size = int_from_bin(read_buffer(8))
        current_size = 0
        while current_size < size:
            inst = INSTRUCTIONS[int_from_bin(read_buffer(1))]
            current_size += 1
            value = '.'
            if inst in SPECIAL_INSTRUCTIONS:
                value = int_from_bin(read_buffer(8))
                current_size += 8
            tape.append((inst, value))
        tapes.append(tape)
    return tapes


def pretty_print(strings, symbols, tapes):
    print "Strings:"
    for i in range(len(strings)):
        print i, binascii.b2a_hex(strings[i]), strings[i]
    print "------------------------------------"
    print "Symbols:"
    for i in range(len(symbols)):
        print i, binascii.b2a_hex(symbols[i]), symbols[i]
    print "------------------------------------"
    print "Tapes:"
    for i in range(len(tapes)):
        print "\tTape "+ str(i)
        for op, value, in tapes[i]:
            print"\t\t"+ op + "\t" + str(value)


def solve(tapes):
    flag = ""
    stack = 0
    for op, value in tapes[0]:
        if value != '.':
            if stack:
                flag += chr(int(value) - stack)
                stack = 0
            else:
                stack = value
    return flag


def main():
    buffer = read_buffer(len(MAGIC))
    if buffer != MAGIC:
        print "Not LISBY file"
        exit(1)
    else:
        strings = read_table()
        symbols = read_table()
        tapes = read_tapes()
        # print strings, symbols, tapes
        buffer = read_buffer(len(MAGIC))
        if buffer != MAGIC[::-1]:
            print "Not LISBY file"
            exit(1)
        pretty_print(strings, symbols, tapes)
    #print solve(tapes)

if __name__ == '__main__':
    main()
