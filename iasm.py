import sys

# cim = computer interpret mode. cem = computer exit mode
modes = {"cim": 0, "cem": 0}
mems = {"map": "", "mbp": "", "mcp": "", "mdp": "", "mep": "", "mfp": "", "mgp": "", "mhp": "",
        "mip": "", "mjp": "", "mkp": ""}
stack = []
labels = {}
memslen = len(mems)

def interpret(code):
    lines = code.split("\n")
    in_label = [False]
    labelname = [""]
    target_mem = ["mbp"]

    for line in lines:
        tokens = line.split() or line.split("\t")

        if tokens:
            token = tokens[0]

            if not in_label[0]:
                if token == "label":
                    labelname[0] = tokens[1]
                    in_label[0] = True
                    labels[labelname[0]] = []
                elif token == "mode":
                    modename = tokens[1]
                    modeskeys = modes.keys()

                    if modename in modeskeys:
                        modevalue = tokens[2]
                        modes[modename] = int(modevalue)
                    else:
                        print("Error: Unknown mode name. Use cim or cem")
                        sys.exit(1)
                elif token == "mov":
                    memname = tokens[1]
                    memskeys = mems.keys()
                    value = tokens[2]
                    if value == "stk":
                        if memname in memskeys:
                            mems[memname] = stack[-1]
                            stack.pop()
                        else:
                            print("Error: Unknown memory point name. You have only from 'map' to 'mkp'.")
                    else:
                        value = int(value)
                        if memname in memskeys:
                            mems[memname] = value
                        else:
                            print("Error: Unknown memory point name. You have only from 'map' to 'mkp'.")
                elif token == "outcall":
                    if modes["cem"] == 1:
                        # if cem is mode 1: print
                        if modes["cim"] == 1:
                            # if cim is mode 1: stack
                            print(stack[-1], end="")
                            stack.pop()
                        elif modes["cim"] == 2:
                            # if cim is mode 2: memory point 'map'
                            print(mems["map"], end="")
                        elif modes["cim"] == 3:
                             # if cim is mode 3: new line
                            print("\n", end="")
                        elif modes["cim"] == 4:
                             # if cim is mode 2: space
                            print(" ", end="")
                        elif modes["cim"] == 5:
                            # if cim is mode 2: target memory point
                            print(mems[target_mem[0]], end="")
                    elif modes["cem"] == 2:
                        # if cem is mode 2: input with
                        if modes["cim"] == 1:
                            # if cim mode is 1: no question to target memory point
                            mems[target_mem[0]] = input()
                        elif modes["cim"] == 2:
                            # if cim mode is 2: question to target memory point
                            mems[target_mem[0]] = input(mems["map"])
                    elif modes["cem"] == 3:
                        # if cem is mode 3: sys exit
                        sys.exit(modes["cim"])
                    modes["cim"] = 0
                    modes["cem"] = 0
                elif token == "push":
                    pushnum = int(tokens[1])
                    stack.append(pushnum)
                elif token == "push_str":
                    string = " ".join(tokens[1:])
                    stack.append(string)
                elif token == "pop":
                    stack.pop()
                elif token == "" or token == ";;":
                    pass
                elif token == "lbl":
                    labelnamee = tokens[1]
                    interpret("\n".join(labels[labelnamee]))
                elif token == "div":
                    num1 = stack[len(stack) - 2]
                    num2 = stack[len(stack) - 1]
                    stack.pop()
                    stack.pop()
                    stack.append(num1 / num2)
                elif token == "sum":
                    num1 = stack[len(stack) - 2]
                    num2 = stack[len(stack) - 1]
                    stack.pop()
                    stack.pop()
                    stack.append(num1 + num2)
                elif token == "sub":
                    num1 = stack[len(stack) - 2]
                    num2 = stack[len(stack) - 1]
                    stack.pop()
                    stack.pop()
                    stack.append(num1 - num2)
                elif token == "mul":
                    num1 = stack[len(stack) - 2]
                    num2 = stack[len(stack) - 1]
                    stack.pop()
                    stack.pop()
                    stack.append(num1 * num2)
                elif token == "inptgt":
                    memname = tokens[1]
                    memskeys = mems.keys()
                    target_mem[0] = memname
                    if memname in memskeys:
                        target_mem[0] = memname
                    else:
                        print("Error: Unknown memory point name. You have only from 'map' to 'mkp'.")
                elif token == "stk":
                    print(stack, end="")
                elif token == "mem":
                    print(mems, end="")
                elif token == "cmp":
                    mem1 = tokens[1]
                    mem2 = tokens[2]
                    labelnamee = tokens[3]
                    if mems.get(mem1) == mems.get(mem2):
                        interpret("\n".join(labels[labelnamee]))
                elif token == "ncmp":
                    mem1 = tokens[1]
                    mem2 = tokens[2]
                    labelnamee = tokens[3]
                    if mems.get(mem1) != mems.get(mem2):
                        interpret("\n".join(labels[labelnamee]))
                elif token == "int":
                    memname = tokens[1]
                    mems[memname] = int(mems[memname])
                elif token == "type":
                    memname = tokens[1]
                    print(type(mems[memname]), end="")
            elif in_label[0]:
                if token == "endlabel":
                    in_label[0] = False
                else:
                    labels[labelname[0]].append(" ".join(tokens))
            
            lemems = len(mems)
            if lemems > memslen:
                print("Error: More memory points has been created!")
                sys.exit(1)
    
if __name__ == "__main__":
    version = "1.0"
    if len(sys.argv) == 1:
        print(f"Interpreted assembly. version: {version}")
        print(f"Usage: {sys.argv[0]} <file>")
    else:
        if sys.argv[1].endswith(".iasm"):
            with open(sys.argv[1], "r") as f:
                interpret(f.read())
        else:
            print("Error: Use .iasm file extension")
