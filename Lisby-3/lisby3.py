import binascii
INSTRUCTIONS = ["HALT","ADD","SUB","MUL","DIV","XOR","MOD","AND","OR","INV","PUSHI","PUSHF","PUSHSTR","PUSHSY","PUSHSYRAW","PUSHTRUE","PUSHFALSE","PUSHUNIT","PUSHCLOSURE","PUSHCONT","QUOTED","POP","CALL","TAILCALL","RET","JT","JF","JMP","STORE","STORETOP","EQ","NEQ","GT","GE","LT","LE","NOT","DECLARE","PRINT","LIST","HEAD","TAIL","LISTCAT","EVAL","DUMP","NEWENV","DEPARTENV"]
SPECIAL_INSTRUCTIONS = ["PUSHI","PUSHF","PUSHSTR","PUSHSY","STORE","STORETOP","PUSHCLOSURE","JT","JF","JMP","DECLARE","LIST","PUSHSYRAW","QUOTED","PUSHCONT"]
MAGIC = "LISBY001"
C = 0
ans = ""
with open("lisby3", "rb") as f:
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

def execute(strings, symbols, tapes):
    # TAPE_INDEX, TAPE_OFFSET
    global ans
    pposos = False
    pc = [0, 0]
    val_stack = []
    call_stack = []
    active_env = list(symbols)
    environments = [active_env]
    closures = {}
    while pc != [0, len(tapes[0])]:
        op, value =  tapes[pc[0]][pc[1]]
        if op == "ADD":
            val_stack.append(val_stack.pop() + val_stack.pop())
        elif op == "SUB":
            val_stack.append(val_stack.pop() - val_stack.pop())
        elif op == "XOR":
            val_stack.append(val_stack.pop() ^ val_stack.pop())
        elif op == "CALL":
            call_stack.append(pc+[len(environments)])
            pc[0] = val_stack.pop()
            pc[1] = 0
            try:
                active_env = closures.pop(len(val_stack) - 1)
            except:
                active_env = list(active_env)
            environments.append(active_env)
        elif op == "DECLARE":
            active_env[value] = ""
        elif op == "DEPARTENV":
            environments.pop()
            active_env = environments[-1]
        elif op == "EQ":
            val_stack.append(val_stack.pop() == val_stack.pop())
        elif op =="HALT":
            print val_stack[-1]
            return
        elif op == "HEAD":
            val_stack.append(val_stack.pop()[0])
        elif op == "JF":
            if val_stack.pop() == False:
                o = 0
                for i in range(len(tapes[pc[0]])):
                    if tapes[pc[0]][i][1] != '.':
                        o += 9
                    else:
                        o += 1
                    if o == value:
                        pc[1] = i
                        break
        elif op == "JT":
            if val_stack.pop() == True:
                o = 0
                for i in range(len(tapes[pc[0]])):
                    if tapes[pc[0]][i][1] != '.':
                        o += 9
                    else:
                        o += 1
                    if o == value:
                        pc[1] = i
                        break
        elif op == "JMP":
            o = 0
            for i in range(len(tapes[pc[0]])):
                if tapes[pc[0]][i][1] != '.':
                    o += 9
                else:
                    o += 1
                if o == value:
                    pc[1] = i
                    break
        elif op == "LIST":
            l = []
            while value:
                l.append(val_stack.pop())
                value -= 1
            val_stack.append(l)
        elif op == "LISTCAT":
            val_stack.append(val_stack.pop() + val_stack.pop())
        elif op == "MOD":
            val_stack.append(val_stack.pop() % val_stack.pop())
        elif op == "NEWENV":
            active_env = list(active_env)
            environments.append(active_env)
        elif op == "POP":
            val_stack.pop()
        elif op == "PRINT":
            print val_stack.pop()
            # try:
            #     ans += chr(int(val_stack.pop()))
            # except:
            #     pass
        elif op == "PUSHFALSE":
            val_stack.append(False)
        elif op == "PUSHTRUE":
            val_stack.append(True)
        elif op == "PUSHCLOSURE":
            closures[len(val_stack)] = list(active_env)
            val_stack.append(value)
        elif op == "PUSHI":
            val_stack.append(value)
        elif op == "PUSHSTR":
            val_stack.append(strings[value])
        elif op == "PUSHUNIT":
            val_stack.append([])
        elif op == "PUSHSY":
            val_stack.append(active_env[value])
        elif op == "RET":
            pop = call_stack.pop()
            pc = pop[:2]
            environments = environments[:pop[2]]
            active_env = environments[-1]
        elif op == "STORE":
            active_env[value] = val_stack.pop()
        elif op == "STORETOP":
            environments[0][value] = val_stack.pop()
        elif op == "TAIL":
            val_stack.append(val_stack.pop()[1:])
        pc[1] += 1

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
    #pretty_print(strings, symbols, tapes)
    execute(strings, symbols, tapes)
