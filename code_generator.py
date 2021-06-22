file_name = "custom_code.txt"

RAM_ADDRESS = 0

code = ""

# CONSTANTS.
REGISTER_A = 0
REGISTER_B = 1
REGISTER_C = 2
REGISTER_ALU_ACCUM = 3
REGISTER_LOGIC_ACCUM = 4
REGISTER_MEMORY_ADDRESS = 5
REGISTER_RAM = 6
REGISTER_ALL_CONDITIONAL_TESTS = 7


OPCODE_STORE_OPERATION = 0
OPCODE_EXECUTE_OPERATION = 1
OPCODE_SET_PC = 2
OPCODE_JUMP_TO_IF_LAST_OP_SMALL = 3
OPCODE_JUMP_TO_IF_LAST_OP_GREATER = 4
OPCODE_JUMP_TO_IF_LAST_OP_EQUAL = 5


NOP = 30
HALT = 31

BUILT_IN_OPERATORS = ["+", "-", "&", "|", ">", "<", ":"]
# (a == b) is represented as (a : b) .
# CONDITIONAL_OPERATORS = ['>', '<', ':']

variables_address_mapping = {}
jump_labels = {}

####INSTRUCTION FORMAT-	 ( 1 ) ( 2 ) (3 4 5 6) ( 7) ( 8 ) th bit from left.
####						L-----|-----|------|-----|-GLOBAL INPUT LINE = INPUT STREAM IF 0.IF 1,INPUT LINE = TEMP REG OUTPUT.
####							  L-----|------|-----|-STORE TO TMP REGISTER. A,B,C ETC CAN WRITE TO OUTPUT LINE,AND IS STORED TO TMP REGISTER.
####							        L------|-----|-INDEX OF REGISTER TO PERFORM OPERATIONS ON.
####									       L-----|-REGISTERS WRITE TO OUTPUT LINE IF 1.
####											     L-REGISTERS READ FROM INPUT LINE IF 1.


def is_number(text):
    for i in range(0, len(text)):
        if i == 0:
            # is_digit() func doesnt take negative numbers into consideration.
            if text[i] == "-":
                continue
        if not text[i].isdigit():
            return False
    return True


def isVariableInRAM(value):
    return value in variables_address_mapping.keys()


def get_address_of_variable(var_name):
    global RAM_ADDRESS

    var_name = var_name.strip()

    if not isVariableInRAM(var_name):
        variables_address_mapping[var_name] = RAM_ADDRESS
        RAM_ADDRESS += 1
    return int(variables_address_mapping[var_name])


def set_input_line_to_ifstream(s):
    p_s = s << 7
    return p_s


def set_write_to_tmp_reg(write_to_temp):
    p_w = write_to_temp << 6
    return p_w


def set_register_index(idx):
    p_idx = idx << 2
    return p_idx


def set_w(w):
    if w > 1:
        print("Error!Way to large")
    p_w = w << 1
    return p_w


def set_r(r):
    if r > 1:
        print("Error!Way to large")
    return r


def get_combined_output(
    set_input_ifstream,
    write_to_temp,
    index,
    reg_write_to_out_line,
    reg_read_from_in_line,
):
    bit1 = set_input_line_to_ifstream(set_input_ifstream)
    bit2 = set_write_to_tmp_reg(write_to_temp)
    bit3_4_5_6 = set_register_index(index)
    bit7 = set_w(reg_write_to_out_line)
    bit8 = set_r(reg_read_from_in_line)

    return bit1 + bit2 + bit3_4_5_6 + bit7 + bit8


def set_register(REGISTER_INDEX, value, param):
    _code = ""
    _code += str(OPCODE_STORE_OPERATION) + " , " + str(param).strip() + "\n"
    _code += str(OPCODE_EXECUTE_OPERATION) + " , " + str(value).strip() + "\n"
    return _code


# The main register writers.
def set_register_value(REGISTER_NAME, value):
    param = get_combined_output(0, 0, REGISTER_NAME, 0, 1)
    # Registers reads from input line.
    return set_register(REGISTER_NAME, value, param)


def set_register_equals_tmp(REGISTER_NAME):
    param = get_combined_output(1, 0, REGISTER_NAME, 0, 1)
    # Registers reads from input line.
    return set_register(REGISTER_NAME, 0, param)


def set_tmp_equals_register(REGISTER_NAME):
    param = get_combined_output(0, 1, REGISTER_NAME, 1, 0)
    return set_register(REGISTER_NAME, 0, param)


def set_jump(LAST_OP, new_program_counter):
    _code = ""
    new_program_counter = str(new_program_counter).strip()
    _code += str(LAST_OP) + " , " + new_program_counter + "\n"
    return _code


# Set registers to the given value.
def set_A(value):
    return set_register_value(REGISTER_A, value)


def set_B(value):
    return set_register_value(REGISTER_B, value)


def set_C(value):
    return set_register_value(REGISTER_C, value)


def set_Memory_Address(value):
    return set_register_value(REGISTER_MEMORY_ADDRESS, value)


def set_RAM(value):
    return set_register_value(REGISTER_RAM, value)


def set_A_equals_tmp():
    return set_register_equals_tmp(REGISTER_A)


def set_B_equals_tmp():
    return set_register_equals_tmp(REGISTER_B)


def set_C_equals_tmp():
    return set_register_equals_tmp(REGISTER_C)


def set_Memory_Address_equals_tmp():
    return set_register_equals_tmp(REGISTER_MEMORY_ADDRESS)


def set_RAM_equals_tmp():
    return set_register_equals_tmp(REGISTER_RAM)


# Set the value of tmp register to the value of the given register.
def set_tmp_equals_A():
    return set_tmp_equals_register(REGISTER_A)


def set_tmp_equals_B():
    return set_tmp_equals_register(REGISTER_B)


def set_tmp_equals_C():
    return set_tmp_equals_register(REGISTER_C)


def set_tmp_equals_Memory_Address():
    return set_tmp_equals_register(REGISTER_MEMORY_ADDRESS)


def set_tmp_equals_RAM():
    return set_tmp_equals_register(REGISTER_RAM)


# Can't be set.
# They are for internal use.
# REGISTER_ALU_ACCUM = 3
# REGISTER_LOGIC_ACCUM = 4
def set_tmp_equals_ALU_ACCUM(op=0):
    param = get_combined_output(0, 1, REGISTER_ALU_ACCUM, 1, 0)
    return set_register(REGISTER_ALU_ACCUM, op, param)


def set_tmp_equals_LOGIC_ACCUM(op=0):
    param = get_combined_output(0, 1, REGISTER_LOGIC_ACCUM, 1, 0)
    return set_register(REGISTER_LOGIC_ACCUM, op, param)


def _set_NOP():
    _code = ""
    _code += str(NOP) + " , " + str(0) + "\n"
    return _code


def _set_HALT():
    _code = ""
    _code += str(HALT) + " , " + str(0) + "\n"
    return _code


def set_jump_if_last_op_small(new_program_counter):
    return set_jump(OPCODE_JUMP_TO_IF_LAST_OP_SMALL, new_program_counter)


def set_jump_if_last_op_greater(new_program_counter):
    return set_jump(OPCODE_JUMP_TO_IF_LAST_OP_GREATER, new_program_counter)


def set_jump_if_last_op_equal(new_program_counter):
    return set_jump(OPCODE_JUMP_TO_IF_LAST_OP_EQUAL, new_program_counter)


# stores all the logical assignments in their own registers.
def set_all_logical_comparisions():
    param = get_combined_output(0, 0, REGISTER_ALL_CONDITIONAL_TESTS, 1, 0)
    return set_register(REGISTER_ALL_CONDITIONAL_TESTS, 0, param)


def write_assignment(var_name, value):
    global code
    address = get_address_of_variable(var_name)
    value = value.strip()

    print("WriteAssignmentFunc:")
    print(value)

    print("is var in ram:")
    print(isVariableInRAM(value))
    print(variables_address_mapping)
    # value can not only be number but another variable itself.
    if is_number(value):
        code += set_Memory_Address(address)
        code += set_RAM(value) + "\n"
    else:
        print("Value is another variable:-->" + value)
        values_address = get_address_of_variable(value)
        code += set_Memory_Address(values_address)
        code += set_tmp_equals_RAM()
        code += set_Memory_Address(address)
        code += set_RAM_equals_tmp() + "\n"


# IF A < 10,
# IF A > 10,
# IF A : 10 MEANS (A == 10)
# IF A < 10 JUMP_T0_LABEL LOOP
# HOW TO IMPLEMENT.
# LOAD A, A
# LOAD B, 10
# WRITE ALL CONDITIONAL_OPERATORS_REGISTERS
# IF SMALL THEN INSTRUCTION, JUMP_T0_LABEL LOOP


def write_add_sub_assignment(result_var_name, var1, var2, operator):
    global code
    # Only if both the vars are another vars in memory.
    result_address = get_address_of_variable(result_var_name)
    var1 = var1.strip()
    var2 = var2.strip()

    op = 0
    if operator == "+":
        op = 0
    if operator == "-":
        op = 1

    isVar1_var_in_ram = isVariableInRAM(var1)
    isVar2_var_in_ram = isVariableInRAM(var2)
    both_are_variables_in_ram = isVar1_var_in_ram and isVar2_var_in_ram

    # Simplify a1+=1 or a1 = a1 + 1

    if both_are_variables_in_ram:
        var1_address = get_address_of_variable(var1)
        var2_address = get_address_of_variable(var2)

        # Load var1 to A.
        code += set_Memory_Address(var1_address)
        code += set_tmp_equals_RAM()
        code += set_A_equals_tmp()

        code += set_Memory_Address(var2_address)
        code += set_tmp_equals_RAM()
        code += set_B_equals_tmp()

        code += set_Memory_Address(result_address)
        code += set_tmp_equals_ALU_ACCUM(op)
        code += set_RAM_equals_tmp()
        code += "\n"
    elif isVar1_var_in_ram:
        # Something like this a1 + 10
        var1_address = get_address_of_variable(var1)
        # Load a1 to A.
        code += set_Memory_Address(var1_address)
        code += set_tmp_equals_RAM()
        code += set_A_equals_tmp()

        code += set_B(int(var2))

        code += set_Memory_Address(result_address)
        code += set_tmp_equals_ALU_ACCUM(op)
        code += set_RAM_equals_tmp()
        code += "\n"
    elif isVar2_var_in_ram:
        # Something like this 10 - a1
        var2_address = get_address_of_variable(var2)
        # Load a1 to A.
        code += set_Memory_Address(var2_address)
        code += set_tmp_equals_RAM()
        code += set_B_equals_tmp()

        code += set_A(int(var1))

        code += set_Memory_Address(result_address)
        code += set_tmp_equals_ALU_ACCUM(op)
        code += set_RAM_equals_tmp()
        code += "\n"
    else:
        # both are constants.
        # Something like this 10 + 10
        code += set_A(int(var1))
        code += set_B(int(var2))

        code += set_Memory_Address(result_address)
        code += set_tmp_equals_ALU_ACCUM(op)
        code += set_RAM_equals_tmp()
        code += "\n"


def write_and_or_assignment(result_var_name, var1, var2, operator):
    global code
    # Only if both the vars are another vars in memory.
    result_address = get_address_of_variable(result_var_name)
    var1 = var1.strip()
    var2 = var2.strip()

    op = 0
    if operator == "&":
        op = 0
    if operator == "|":
        op = 1

    isVar1_var_in_ram = isVariableInRAM(var1)
    isVar2_var_in_ram = isVariableInRAM(var2)
    both_are_variables_in_ram = isVar1_var_in_ram and isVar2_var_in_ram

    if both_are_variables_in_ram:
        var1_address = get_address_of_variable(var1)
        var2_address = get_address_of_variable(var2)

        # Load var1 to A.
        code += set_Memory_Address(var1_address)
        code += set_tmp_equals_RAM()
        code += set_A_equals_tmp()

        code += set_Memory_Address(var2_address)
        code += set_tmp_equals_RAM()
        code += set_B_equals_tmp()

        code += set_Memory_Address(result_address)
        code += set_tmp_equals_LOGIC_ACCUM(op)
        code += set_RAM_equals_tmp()
        code += "\n"
    elif isVar1_var_in_ram:
        # Something like this a1 + 10
        var1_address = get_address_of_variable(var1)
        # Load a1 to A.
        code += set_Memory_Address(var1_address)
        code += set_tmp_equals_RAM()
        code += set_A_equals_tmp()

        code += set_B(int(var2))

        code += set_Memory_Address(result_address)
        code += set_tmp_equals_LOGIC_ACCUM(op)
        code += set_RAM_equals_tmp()
        code += "\n"
    elif isVar2_var_in_ram:
        # Something like this 10 - a1
        var2_address = get_address_of_variable(var2)
        # Load a1 to A.
        code += set_Memory_Address(var2_address)
        code += set_tmp_equals_RAM()
        code += set_B_equals_tmp()

        code += set_A(int(var1))

        code += set_Memory_Address(result_address)
        code += set_tmp_equals_LOGIC_ACCUM(op)
        code += set_RAM_equals_tmp()
        code += "\n"
    else:
        # both are constants.
        # Something like this 10 + 10
        code += set_A(int(var1))
        code += set_B(var2)

        code += set_Memory_Address(result_address)
        code += set_tmp_equals_LOGIC_ACCUM(op)
        code += set_RAM_equals_tmp()
        code += "\n"


def write_conditional_assignment(var1, var2, operator):
    global code
    # Only if both the vars are another vars in memory.
    var1 = var1.strip()
    var2 = var2.strip()
    # every operators result is calculated at once in their own register's.
    op = 0

    isVar1_var_in_ram = isVariableInRAM(var1)
    isVar2_var_in_ram = isVariableInRAM(var2)
    both_are_variables_in_ram = isVar1_var_in_ram and isVar2_var_in_ram

    if both_are_variables_in_ram:
        var1_address = get_address_of_variable(var1)
        var2_address = get_address_of_variable(var2)

        # Load var1 to A.
        code += set_Memory_Address(var1_address)
        code += set_tmp_equals_RAM()
        code += set_A_equals_tmp()

        code += set_Memory_Address(var2_address)
        code += set_tmp_equals_RAM()
        code += set_B_equals_tmp()

        code += set_all_logical_comparisions()

        code += "\n"
    elif isVar1_var_in_ram:
        # Something like this a1 + 10
        var1_address = get_address_of_variable(var1)
        # Load a1 to A.
        code += set_Memory_Address(var1_address)
        code += set_tmp_equals_RAM()
        code += set_A_equals_tmp()

        code += set_B(int(var2))

        code += set_all_logical_comparisions()

        code += "\n"
    elif isVar2_var_in_ram:
        # Something like this 10 - a1
        var2_address = get_address_of_variable(var2)
        # Load a1 to A.
        code += set_Memory_Address(var2_address)
        code += set_tmp_equals_RAM()
        code += set_B_equals_tmp()

        code += set_A(int(var1))

        code += set_all_logical_comparisions()

        code += "\n"
    else:
        # both are constants.
        # Something like this 10 + 10
        code += set_A(int(var1))
        code += set_B(var2)

        code += set_all_logical_comparisions()

        code += "\n"


def write_arithmatic_assignment(result_var_name, var1, var2, p_op):
    result_var_name = result_var_name.strip()
    var1 = var1.strip()
    var2 = var2.strip()
    p_op = p_op.strip()
    print(p_op)

    if p_op == "+" or p_op == "-":
        print("add_sub_op")
        write_add_sub_assignment(result_var_name, var1, var2, p_op)
        return

    if p_op == "&" or p_op == "|":
        print("and_or_op")
        write_and_or_assignment(result_var_name, var1, var2, p_op)
        return

    # CONDITIONAL_OPERATORS = ['>', '<', ':']
    if p_op == ">" or p_op == "<" or p_op == ":":
        print("conditional_operator")
        write_conditional_assignment(var1, var2, p_op)
        return


def write_NOP():
    global code
    code += _set_NOP() + "\n"


def write_halt():
    global code
    code += _set_HALT() + "\n"


def _set_program_counter(pc):
    _code = ""
    _code += str(OPCODE_SET_PC) + " , " + str(pc) + "\n"
    return _code


# write in ascii,probably to modify it next pass.
def write_text_code(p_code):
    global code
    code += p_code


def write_jump_back_label():
    global code
    code += _set_program_counter(label_position) + "\n"


def simplify_equation(big_eqn):
    line = big_eqn.strip()

    if "=" in line:
        # Assignment statement.
        main_var_name, value = line.split("=")
        value = value.strip()

        vars = []
        operators = []

        index = 0
        size = len(value)
        varname = ""
        for char in value:
            if char in BUILT_IN_OPERATORS:
                print("char is built in operator")
                operators.append(char)
                varname = varname.strip()
                vars.append(varname)
                varname = ""
            else:
                varname = varname + char
                if index >= (size - 1):
                    # last char and we are still adding char to varname.
                    # so write them now.
                    varname = varname.strip()
                    vars.append(varname)
            index += 1

        if not (len(operators) >= 1):
            main_var_name = main_var_name.strip()
            value = value.strip()
            return main_var_name + " = " + value + "\n"

        print("Vars:")
        for var in vars:
            print(var)
        print("\n")
        print("Operators:")
        for op in operators:
            print(op)
        print("\n")
        print("New code:\nTotal vars:")
        # main_var_name
        main_var_name = main_var_name.strip()
        total_vars = len(vars)
        print(total_vars)

        code = ""

        if total_vars >= 2:
            c = 0
            for i in range(0, total_vars - 1, 1):
                if total_vars - 1 > 1:
                    first_tmp_var = main_var_name + "" + str(i)
                else:
                    first_tmp_var = main_var_name
                # if we have only two vars then
                # no need to create new var name.

                if i == 0:
                    code += (
                        first_tmp_var
                        + " = "
                        + vars[i]
                        + " "
                        + operators[i]
                        + " "
                        + vars[i + 1]
                        + "\n"
                    )

                else:
                    last_tmp_var = main_var_name + "" + str(i - 1)
                    code += (
                        first_tmp_var
                        + " = "
                        + last_tmp_var
                        + " "
                        + operators[i]
                        + " "
                        + vars[i + 1]
                        + "\n"
                    )

            if total_vars - 1 > 1:
                # set all th values to their initial variable.
                i = total_vars - 1
                last_tmp_var = main_var_name + "" + str(i - 1)
                code += main_var_name + " = " + last_tmp_var + "\n"

        # else:
        # 	code += main_var_name + "=" + vars

        print("Gen code:")
        print(code)
        return code

    return "\n"


simplified_code = ""
loop_details = {}
count = 0

# First Pass, simplifiy the code.
with open(file_name) as fp:
    Lines = fp.readlines()
    for line in Lines:
        count += 1
        line = line.strip()
        print("Line{}: {}".format(count, line))

        if "=" in line and (not line.startswith("FOR")):
            if "+=" in line:
                var_name, value = line.split("+=")
                var_name = var_name.strip()
                value = value.strip()
                simplified_code += var_name + " = " + var_name + " + " + value + "\n"
            elif "-=" in line:
                var_name, value = line.split("-=")
                var_name = var_name.strip()
                value = value.strip()
                simplified_code += var_name + " = " + var_name + " - " + value + "\n"
            else:
                simplified_code += simplify_equation(line)
        elif line.startswith("FOR"):
            all_tokens = line.split(" ")
            loop_name = ""
            loop_begin = ""
            loop_end = ""
            loop_step = ""
            # x = "FOR I = 1 TO 10 STEP 1"
            # z = x.split(" ")
            # z ----->['FOR', 'I', '=', '1', 'TO', '10', 'STEP', '1']
            print("Begin of a for loop \n\n\n\n\n\n\n\n\n")
            if len(all_tokens) >= 6:
                contains_loop = all_tokens[0] == "FOR"
                contains_equal = all_tokens[2] == "="
                contains_to = all_tokens[4] == "TO"

                if contains_loop and contains_equal and contains_to:
                    print("A valid FOR loop detected")
                    loop_name = all_tokens[1]
                    # all_tokens[2] = "="
                    loop_begin = all_tokens[3]
                    # all_tokens[4] = "TO"
                    loop_end = all_tokens[5]

                    if len(all_tokens) == 8:
                        contains_step = all_tokens[6] == "STEP"
                        if contains_step:
                            loop_step = all_tokens[7]

                    # Save them.
                    loop_label_name = "LOOP_" + loop_name
                    loop_details[loop_name] = [
                        loop_label_name,
                        loop_begin,
                        loop_end,
                        loop_step,
                    ]

                    # I = 0
                    # LABEL LOOP1

                    simplified_code += loop_name + " = " + loop_begin + "\n"
                    simplified_code += "LABEL " + loop_label_name + "\n"
        elif line.startswith("NEXT"):
            all_tokens = line.split(" ")
            if len(all_tokens) == 2:
                if all_tokens[0] == "NEXT":
                    loop_name_end = all_tokens[1]
                    if loop_name_end in loop_details.keys():
                        print("End of a valid loop")
                        p_loop_details = loop_details[loop_name_end]
                        p_loop_label = p_loop_details[0]
                        p_loop_begin = p_loop_details[1]
                        p_loop_end = p_loop_details[2]
                        p_loop_step = p_loop_details[3]
                        # I = I + 1
                        # Z = I < 10
                        # JUMP_TO_IF_LAST_OP_SMALL LOOP1

                        # p_loop_details is in this format : "LOOP_1"
                        _, id = p_loop_label.split("_")
                        simplified_code += id + " = " + id + " + " + p_loop_step + "\n"
                        simplified_code += (
                            "tmp_condition_check_var = "
                            + id
                            + " < "
                            + p_loop_end
                            + "\n"
                        )
                        simplified_code += (
                            "JUMP_TO_IF_LAST_OP_SMALL " + p_loop_label + "\n"
                        )

        else:
            simplified_code += line + "\n"

s_c_f = open("simplified_code.txt", "w")
s_c_f.write(simplified_code)
s_c_f.close()


# generate_code
# with open(file_name) as fp:
count = 0

with open("simplified_code.txt") as fp:

    Lines = fp.readlines()
    for line in Lines:
        count += 1
        line = line.strip()
        print("Line {} : {}".format(count, line))

        if "=" in line:
            # Assignment statement.
            var_name, value = line.split("=")
            var_name = var_name.strip()
            value = value.strip()

            containsAdditionalOperators = False
            p_op = ""
            for char in value:
                if char in BUILT_IN_OPERATORS:
                    p_op = char
                    containsAdditionalOperators = True
                    break

            if containsAdditionalOperators:
                print("Arithmatic assignent")
                print("value before splittin:" + value)
                var_1, var_2 = value.split(p_op)
                var_1 = var_1.strip()
                var_2 = var_2.strip()
                print("var1 : " + var_1 + " var2 : " + var_2)
                write_arithmatic_assignment(var_name, var_1, var_2, p_op)
            else:
                # just a normal assignment.
                write_assignment(var_name, value)

        if line == "NOP":
            write_NOP()
        elif line == "HALT":
            write_halt()
        elif line.startswith("LABEL"):
            # Do it next pass.
            # label_position = count - 1
            write_text_code(line + "\n")
        elif line == "JUMP_T0_LABEL":
            write_text_code(line + "\n")
            # print("Jump back:" + str(label_position))
            # write_jump_back_label()
        elif line.startswith("JUMP_TO_IF_LAST_OP_SMALL"):
            write_text_code(line + "\n")

# print(code)

gen_code_file = "generated_code.txt"

f = open(gen_code_file, "w")
f.write(code)
f.close()


# Get all labels and store their position.
index = 0
with open(gen_code_file) as fp:
    Lines = fp.readlines()
    for line in Lines:

        if (not line) or (line == "") or (line == "\n"):
            continue

        if line.startswith("LABEL"):
            _, label_name = line.split(" ")
            label_name = label_name.strip()
            label_pos = index
            print("Found a label with name : " + str(label_name))
            print("With Index : " + str(label_pos))

            # Save it in a list.
            if label_name in jump_labels.keys():
                print("Error..Redeclaration of label")
            else:
                jump_labels[label_name] = label_pos
            continue

        index += 1

# Now, check if there are jump_to instructions for the corresponding label.
index = 0
with open(gen_code_file) as fp:
    Lines = fp.readlines()
    for line in Lines:

        if (not line) or (line == "") or (line == "\n"):
            continue

        if line.startswith("JUMP_TO_IF_LAST_OP_SMALL"):
            _, target_label = line.split(" ")
            target_label = target_label.strip()

            if target_label in jump_labels.keys():
                print("Label Available : " + str(target_label))

        index += 1


# Write the final binary to corresponding hex files.
# These hex files should be loaded to the ROM module in 'Digital' software.

code_hex_file = "code.hex"
data_hex_file = "data.hex"


file_code = open(code_hex_file, "w")
file_data = open(data_hex_file, "w")

from intelhex import IntelHex

ih_code = IntelHex()
ih_data = IntelHex()

instruction_counter = 0

with open(gen_code_file) as fp:
    Lines = fp.readlines()
    for line in Lines:

        if (not line) or (line == "") or (line == "\n"):
            continue

        line = line.strip()

        if line.startswith("LABEL"):
            # Just skip.
            continue

        if line.startswith("JUMP_TO_IF_LAST_OP_SMALL"):
            _, target_label = line.split(" ")
            target_label = target_label.strip()

            if target_label in jump_labels.keys():
                label_position = jump_labels[target_label]
                line = set_jump_if_last_op_small(label_position)
                line = line.strip()
                print("generate_code for jump if small: " + line)
            else:
                print("Error..Jumping")
                continue

        string1, string2 = line.split(",")

        string1 = string1.strip()
        ih_code[instruction_counter] = int(string1)

        string2 = string2.strip()
        ih_data[instruction_counter] = int(string2)

        instruction_counter += 1


print(ih_code)
ih_code.write_hex_file(file_code)
ih_data.write_hex_file(file_data)

file_code.close()
file_data.close()

print("Total instructions:" + str(instruction_counter))
