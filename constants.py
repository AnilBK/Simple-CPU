# CONSTANTS.
ID_REGISTER_A = 0
ID_REGISTER_B = 1
ID_REGISTER_C = 2
ID_REGISTER_ALU_ACCUM = 3
ID_REGISTER_LOGIC_ACCUM = 4
ID_REGISTER_MEMORY_ADDRESS = 5
ID_REGISTER_RAM = 6
ID_REGISTER_ALL_CONDITIONAL_TESTS = 7
ID_REGISTER_SIMD_A1 = 8
ID_REGISTER_SIMD_B1 = 9
ID_REGISTER_EXECUTE_SIMD = 10
ID_REGISTER_SIMD_A2 = 11
ID_REGISTER_SIMD_B2 = 12

NOP = 30
HALT = 31

OPCODE_STORE_OPERATION = 0
OPCODE_EXECUTE_OPERATION = 1
OPCODE_SET_PC = 2
OPCODE_JUMP_TO_IF_LAST_OP_SMALL = 3
OPCODE_JUMP_TO_IF_LAST_OP_GREATER = 4
OPCODE_JUMP_TO_IF_LAST_OP_EQUAL = 5


BUILT_IN_OPERATORS = ["+", "-", "&", "|", ">", "<", ":"]
# (a == b) is represented as (a : b) .
# CONDITIONAL_OPERATORS = ['>', '<', ':']


def is_number(text):
    for i in range(0, len(text)):
        if i == 0:
            # is_digit() func doesnt take negative numbers into consideration.
            if text[i] == "-":
                continue
        if not text[i].isdigit():
            return False
    return True
