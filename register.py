from constants import *


####INSTRUCTION FORMAT-	 ( 1 ) ( 2 ) (3 4 5 6) ( 7) ( 8 ) th bit from left.
####                        L-----|-----|------|-----|-GLOBAL INPUT LINE = INPUT STREAM, IF 0.IF 1,INPUT LINE = TEMP REG OUTPUT.
####                              L-----|------|-----|-STORE TO TMP REGISTER. A,B,C ETC CAN WRITE TO OUTPUT LINE,AND IS STORED TO TMP REGISTER.
####                                    L------|-----|-INDEX OF REGISTER TO PERFORM OPERATIONS ON.
####                                           L-----|-REGISTERS WRITE TO OUTPUT LINE IF 1.
####                                                 L-REGISTERS READ FROM INPUT LINE IF 1.
def encode_inputs(
    set_input_ifstream,
    write_to_temp_reg,
    set_register_index,
    reg_write_to_out_line,
    reg_read_from_in_line,
):
    if reg_write_to_out_line > 1 or reg_read_from_in_line > 1:
        raise Exception("r/w line should be just 1 bit.")

    bit1 = set_input_ifstream << 7
    bit2 = write_to_temp_reg << 6
    bit3_4_5_6 = set_register_index << 2
    bit7 = reg_write_to_out_line << 1
    bit8 = reg_read_from_in_line

    return bit1 + bit2 + bit3_4_5_6 + bit7 + bit8


def emit_code(value, param):
    _code = ""
    _code += str(OPCODE_STORE_OPERATION) + " , " + str(param).strip() + "\n"
    _code += str(OPCODE_EXECUTE_OPERATION) + " , " + str(value).strip() + "\n"
    return _code


class Register:
    def __init__(self, REGISTER_ID) -> None:
        self.REGISTER_ID = REGISTER_ID

    def equals(self, value):
        param = encode_inputs(0, 0, self.REGISTER_ID, 0, 1)
        return emit_code(value, param)

    def equals_tmp(self):
        # Registers reads from input line.
        param = encode_inputs(1, 0, self.REGISTER_ID, 0, 1)
        return emit_code(0, param)


##################################################################################
##################################################################################
##################################################################################

# Tmp register is defined separately then other general purpose registers.
def set_tmp_equals_(register):
    param = encode_inputs(0, 1, register.REGISTER_ID, 1, 0)
    return emit_code(0, param)


def set_tmp_equals_ALU_ACCUM(op=0):
    param = encode_inputs(0, 1, ID_REGISTER_ALU_ACCUM, 1, 0)
    return emit_code(op, param)


def set_tmp_equals_LOGIC_ACCUM(op=0):
    param = encode_inputs(0, 1, ID_REGISTER_LOGIC_ACCUM, 1, 0)
    return emit_code(op, param)
