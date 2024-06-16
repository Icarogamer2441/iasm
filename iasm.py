import sys
import os

# cim = computer interpret mode. cem = computer exit mode
modes = {"cim": 0, "cem": 0}
mems = {"map": "", "mbp": "", "mcp": "", "mdp": "", "mep": "", "mfp": "", "mgp": "", "mhp": "",
        "mip": "", "mjp": "", "mkp": "", "nl": "\n", "spc": " "}
stack = []
labels = {}
memslen = len(mems)

# made by chatgpt
def search_iasmimport(current_dir):
    # Check if we are in the iasmimport directory
    if os.path.exists(os.path.join(current_dir, 'iasmimport')):
        return os.path.join(current_dir, 'iasmimport')
    
    # Check if we have reached the root of the filesystem
    if os.path.abspath(current_dir) == os.path.abspath(os.sep):
        return None
    
    # Try the parent directory
    parent_dir = os.path.dirname(current_dir)
    return search_iasmimport(parent_dir)

def process_import(libname):
    # Search for the iasmimport directory
    iasm_dir = search_iasmimport(os.getcwd())
    
    if iasm_dir is None:
        print('Error: "iasmimport" directory not found.')
        return
    
    # Check if there is a .iasm file in the iasmimport directory
    for filename in os.listdir(iasm_dir):
        if filename.endswith('.iasm') and libname == filename:
            with open(filename, "r") as fi:
                interpret(fi.read())

# made by me:
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
                elif token == "read":
                    filememname = tokens[1]
                    with open(mems[filememname], "r") as fi:
                        stack.append(fi.read())
                elif token == "write":
                    filememname = tokens[1]
                    with open(mems[filememname], "w") as fi:
                        fi.write(stack[-1])
                        stack.pop()
                elif token == "append":
                    filememname = tokens[1]
                    with open(mems[filememname], "a") as fi:
                        fi.write(stack[-1])
                        stack.pop()
                elif token == "appendnl":
                    filememname = tokens[1]
                    with open(mems[filememname], "a") as fi:
                        fi.write("\n")
                elif token == "readimport":
                    filename = tokens[1]
                    if filename.endswith(".iasm"):
                        with open(filename, "r") as fi:
                            interpret(fi.read())
                    else:
                        print("Error: Use .iasm file extension")
                elif token == "import":
                    libname = tokens[1]
                    process_import(libname)
                elif token == "joinspc":
                    memname = tokens[1]
                    mems[memname] = stack[len(stack) - 2] + " " + stack[len(stack) - 1]
                    stack.pop()
                    stack.pop()
                elif token == "join":
                    memname = tokens[1]
                    mems[memname] = stack[len(stack) - 2] + stack[len(stack) - 1]
                    stack.pop()
                    stack.pop()
                elif token == "joinnl":
                    memname = tokens[1]
                    mems[memname] = stack[len(stack) - 2] + "\n" + stack[len(stack) - 1]
                    stack.pop()
                    stack.pop()
                elif token == "joinspcmem":
                    memname1 = tokens[1]
                    memname2 = tokens[2]
                    mems[memname1] = mems.get(memname1) + " " + mems.get(memname2)
                elif token == "joinmem":
                    memname1 = tokens[1]
                    memname2 = tokens[2]
                    mems[memname1] = mems.get(memname1) + mems.get(memname2)
                elif token == "joinmemnl":
                    memname1 = tokens[1]
                    memname2 = tokens[2]
                    mems[memname1] = mems.get(memname1) + "\n" + mems.get(memname2)
                elif token == "stack":
                    memname = tokens[1]
                    stack.append(mems.get(memname))
                    mems[memname] = ""
                elif token == "memimport":
                    memfilename = tokens[1]
                    if mems.get(memfilename).endswith(".iasm"):
                        with open(mems.get(memfilename), "r") as fi:
                            interpret(fi.read())
                    else:
                        print("Error: Use .iasm file extension")
                else:
                    print(f"Error: unkown token '{token}'.")
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
    version = "1.1"
    if len(sys.argv) == 1:
        print(f"Interpreted assembly. version: {version}")
        print(f"Usage: {sys.argv[0]} <file>")
    else:
        if sys.argv[1].endswith(".iasm"):
            with open(sys.argv[1], "r") as f:
                interpret(f.read())
        else:
            print("Error: Use .iasm file extension")
