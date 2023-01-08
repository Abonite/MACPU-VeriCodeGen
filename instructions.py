IN = "0"
OUT = "1"

DISABLE = "0"
ENABLE = "1"

VALID = "1"
INVALID = "0"

INT_PRI_AB = "0"
INT_PRI_BA = "0"
INT_ADDR_SET_DISABLE = "2'b00"
INT_ADDR_SET_INTA = "2'b01"
INT_ADDR_SET_INTB = "2'b10"
INT_ADDR_RESET = "3'b11"
INT_NUM_DATAMUX = "datamux[4:0]"

DATAMUX = "datamux"

ZERO_ADDRESS = "16'b0"

REG_A = "4'h1"
REG_B = "4'h2"
REG_C = "4'h3"
REG_D = "4'h4"
REG_E = "4'h5"
REG_F = "4'h6"
REG_R = "4'h7"
REG_SS = "4'h7"
REG_SP = "4'h8"
REG_IMDN = "4'h8"
REG_NULL = "4'h0"


class IO:
    rw = IN
    lock = IN

    def __init__(self, rw=IN, lock=IN):
        """----------IO----------
        rw: When executing this instruction, specify whether the cpu writes
            data or reads data in this code
        lock: When executing this instruction, specify whether the lock pin
            of the cpu is input or output"""
        self.rw = rw
        self.lock = lock

    def io_control_code(self) -> str:
        iocc = [self.lock, self.rw]
        iocc_str = "".join(iocc)

        return f"{len(iocc)}'b{iocc_str}"


class PC:
    setpc = DISABLE
    output = ENABLE
    lock = DISABLE

    def __init__(self, setpc=DISABLE, output=ENABLE, lock=DISABLE):
        """----------PC----------
        set: Set PC to the value of the current data lineset pc
        output: Allow PC to output address to address bus
        lock: Lock PC so it no longer self-expands"""
        self.setpc = setpc
        self.output = output
        self.lock = lock

    def pc_control_code(self) -> str:
        pccc = [self.lock, self.output, self.setpc]
        pccc_str = "".join(pccc)

        return f"{len(pccc)}'b{pccc_str}"


class DC:
    data_io = IN
    data_enable = ENABLE
    address_output = DISABLE
    lock = DISABLE
    address = ZERO_ADDRESS
    alu_data = "16'h0"

    def __init__(
        self,
        data_io=IN,
        data_enable=ENABLE,
        address_output=DISABLE,
        address=ZERO_ADDRESS,
        lock=DISABLE,
        alu_data="16'h0"
    ):
        """ ----------DC----------
        data_io: Determines whether the decoder is currently reading or writing
            data from the address bus
        data_enable: Specifies whether the input and output data of the decoder
            is valid
        address_output: Whether to use the address value provided by the
            decoder (useful with instructions such as jumps, used with address
            settings)
        lock: Lock the decoder to suspend its operation
        address: Value of address when output address is valid"""
        self.data_io = data_io
        self.data_enable = data_enable
        self.address_output = address_output
        self.address = address
        self.lock = lock
        self.alu_data = alu_data

    def dc_control_code(self) -> str:
        dccc = [self.lock, self.address_output, self.data_enable, self.data_io]
        dccc_str = "".join(dccc)

        return f"{len(dccc)}'b{dccc_str}"

    def get_dc_address(self) -> str:
        return self.address

    def get_alu_data(self) -> str:
        return self.alu_data


class CT:
    inta_en = DISABLE
    intb_en = DISABLE
    int_priority = INT_PRI_AB
    set_info_en = DISABLE
    set_addr_op = INT_ADDR_SET_DISABLE
    soft_int_valid = INVALID
    soft_int_num = "5'b0"
    recover_pc = DISABLE

    def __init__(
        self,
        inta_en=DISABLE,
        intb_en=DISABLE,
        int_priority=INT_PRI_AB,
        set_info_en=DISABLE,
        set_addr_op=INT_ADDR_SET_DISABLE,
        soft_int_valid=INVALID,
        soft_int_num="5'b0",
        recover_pc=DISABLE
    ):
        self.inta_en = inta_en
        self.intb_en = intb_en
        self.int_priority = int_priority
        self.set_info_en = set_info_en
        self.set_addr_op = set_addr_op
        self.soft_int_valid = soft_int_valid
        self.soft_int_num = soft_int_num
        self.recover_pc = recover_pc

    def ct_control_code(self) -> str:
        hard_int_set = "".join([
            self.set_info_en,
            self.int_priority,
            self.intb_en,
            self.inta_en
        ])
        ctcc = ", ".join([
            f"1'b{self.recover_pc}",
            self.soft_int_num,
            f"1'b{self.soft_int_valid}",
            self.set_addr_op,
            f"4'b{hard_int_set}"
        ])

        return "{" + ctcc + "}"


class ALU:
    direct_io = IN
    direct_io_en = DISABLE
    decoder_io_en = DISABLE
    rega = REG_NULL
    regb = REG_NULL
    operate_code = "8'b0"

    def __init__(
        self,
        direct_io=IN,
        direct_io_en=DISABLE,
        decoder_io_en=DISABLE,
        rega=REG_NULL,
        regb=REG_NULL,
        operate_code="8'b0"
    ):
        self.direct_io = direct_io
        self.direct_io_en = direct_io_en
        self.decoder_io_en = decoder_io_en
        self.rega = rega
        self.regb = regb
        self.operate_code = operate_code

    def alu_control_code(self) -> str:
        alu_io_cc = "".join([
            self.decoder_io_en,
            self.direct_io_en,
            self.direct_io
        ])

        alucc = ", ".join([
            self.operate_code,
            self.regb,
            self.rega,
            f"3'b{alu_io_cc}"
        ])

        return "{" + alucc + "}"


class NOP:
    arg_name = "NOP"
    base_bin_code = 0
    arg_num = 0
    alu_op = False
    next_state = "INST"

    def __init__(self):
        self.io = IO()
        self.pc = PC()
        self.dc = DC()
        self.ct = CT()
        self.alu = ALU()


class MOV:
    arg_name = "MOV"
    base_bin_code = 1
    arg_num = 2
    alu_op = True
    append_args = [
        (
            "addr",
            "regs",
            0,
            "IO_ARGA",
            IO(),
            PC(output=DISABLE, lock=ENABLE),
            DC(data_enable=DISABLE, address_output=ENABLE, address="arga"),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega="argb[3:0]",
                operate_code="inst[7:0]"
            ),
        ),
        (
            "regs",
            "regs",
            1,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                regb="argb[3:0]",
                operate_code="inst[7:0]"
            ),
        ),
        (
            "regs",
            "addr",
            2,
            "IO_ARGA",
            IO(rw=OUT, lock=OUT),
            PC(output=DISABLE, lock=ENABLE),
            DC(data_enable=DISABLE, address_output=ENABLE, address="argb"),
            CT(),
            ALU(
                direct_io=OUT,
                direct_io_en=ENABLE,
                rega="arga[3:0]",
                operate_code="inst[7:0]"
            )
        ),
    ]

    def __init__(self):
        pass


class LOAD:
    arg_name = "LOAD"
    base_bin_code = 4
    arg_num = 2
    alu_op = True
    append_args = [
        (
            "imdn",
            "regs",
            0,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(alu_data="arga"),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega="datamux[3:0]",
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class ADD:
    arg_name = "ADD"
    base_bin_code = 0x10
    arg_num = 2
    alu_op = True
    append_args = [
        (
            "regs",
            "regs",
            0x0,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                regb="datamux[3:0]",
                operate_code="inst[7:0]"
            )
        ),
        (
            "regs",
            "imdn",
            0x100,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega="arga[3:0]",
                regb=REG_IMDN,
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class SUB:
    arg_name = "SUB"
    base_bin_code = 0x11
    arg_num = 2
    alu_op = True
    append_args = [
        (
            "regs",
            "regs",
            0x0,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                regb="datamux[3:0]",
                operate_code="inst[7:0]"
            )
        ),
        (
            "regs",
            "imdn",
            0x100,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega="arga[3:0]",
                regb=REG_IMDN,
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class AND:
    arg_name = "AND"
    base_bin_code = 0x12
    arg_num = 2
    alu_op = True
    append_args = [
        (
            "regs",
            "regs",
            0x0,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                regb="datamux[3:0]",
                operate_code="inst[7:0]"
            )
        ),
        (
            "regs",
            "imdn",
            0x100,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega="arga[3:0]",
                regb=REG_IMDN,
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class OR:
    arg_name = "OR"
    base_bin_code = 0x13
    arg_num = 2
    alu_op = True
    append_args = [
        (
            "regs",
            "regs",
            0x0,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                regb="datamux[3:0]",
                operate_code="inst[7:0]"
            )
        ),
        (
            "regs",
            "imdn",
            0x100,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega="arga[3:0]",
                regb=REG_IMDN,
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class NOT:
    arg_name = "NOT"
    base_bin_code = 0x14
    arg_num = 2
    alu_op = True
    append_args = [
        (
            "regs",
            "regs",
            0x0,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                regb="datamux[3:0]",
                operate_code="inst[7:0]"
            )
        ),
        (
            "regs",
            "imdn",
            0x100,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega="arga[3:0]",
                regb=REG_IMDN,
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class XOR:
    arg_name = "XOR"
    base_bin_code = 0x15
    arg_num = 2
    alu_op = True
    append_args = [
        (
            "regs",
            "regs",
            0x0,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                regb="datamux[3:0]",
                operate_code="inst[7:0]"
            )
        ),
        (
            "regs",
            "imdn",
            0x100,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega="arga[3:0]",
                regb=REG_IMDN,
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class RAND:
    arg_name = "RAND"
    base_bin_code = 0x16
    arg_num = 1
    alu_op = True
    append_args = [
        (
            "regs",
            0x0,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                operate_code="inst[7:0]"
            )
        ),
        (
            "imdn",
            0x100,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega=REG_IMDN,
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class ROR:
    arg_name = "ROR"
    base_bin_code = 0x17
    arg_num = 1
    alu_op = True
    append_args = [
        (
            "regs",
            0x0,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                operate_code="inst[7:0]"
            )
        ),
        (
            "imdn",
            0x100,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega=REG_IMDN,
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class RXOR:
    arg_name = "RXOR"
    base_bin_code = 0x18
    arg_num = 1
    alu_op = True
    append_args = [
        (
            "regs",
            0x0,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                operate_code="inst[7:0]"
            )
        ),
        (
            "imdn",
            0x100,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega=REG_IMDN,
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class LSL:
    arg_name = "LSL"
    base_bin_code = 0x19
    arg_num = 1
    alu_op = True
    append_args = [
        (
            "regs",
            0x0,
            "ONE_ARG",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                operate_code="inst[7:0]"
            )
        ),
        (
            "imdn",
            0x100,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega=REG_IMDN,
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class LSR:
    arg_name = "LSR"
    base_bin_code = 0x1A
    arg_num = 1
    alu_op = True
    append_args = [
        (
            "regs",
            0x0,
            "ONE_ARG",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                operate_code="inst[7:0]"
            )
        ),
        (
            "imdn",
            0x100,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega=REG_IMDN,
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class ASL:
    arg_name = "ASL"
    base_bin_code = 0x1B
    arg_num = 1
    alu_op = True
    append_args = [
        (
            "regs",
            0x0,
            "ONE_ARG",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                operate_code="inst[7:0]"
            )
        ),
        (
            "imdn",
            0x100,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega=REG_IMDN,
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class ASR:
    arg_name = "ASR"
    base_bin_code = 0x1C
    arg_num = 1
    alu_op = True
    append_args = [
        (
            "regs",
            0x0,
            "ONE_ARG",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                operate_code="inst[7:0]"
            )
        ),
        (
            "imdn",
            0x100,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega=REG_IMDN,
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class CSL:
    arg_name = "CSL"
    base_bin_code = 0x1D
    arg_num = 1
    alu_op = True
    append_args = [
        (
            "regs",
            0,
            "ONE_ARG",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                operate_code="inst[7:0]"
            )
        ),
        (
            "imdn",
            0x100,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega=REG_IMDN,
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class CSR:
    arg_name = "CSR"
    base_bin_code = 0x1E
    arg_num = 1
    alu_op = True
    append_args = [
        (
            "regs",
            0x0,
            "ONE_ARG",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                operate_code="inst[7:0]"
            )
        ),
        (
            "imdn",
            0x100,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                direct_io_en=ENABLE,
                rega=REG_IMDN,
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class INC:
    arg_name = "INC"
    base_bin_code = 0x1F
    arg_num = 1
    alu_op = True
    append_args = [
        (
            "regs",
            0,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class DEC:
    arg_name = "DEC"
    base_bin_code = 0x20
    arg_num = 1
    alu_op = True
    append_args = [
        (
            "regs",
            0,
            "TWO_ARGA",
            IO(),
            PC(),
            DC(),
            CT(),
            ALU(
                rega="arga[3:0]",
                operate_code="inst[7:0]"
            )
        )
    ]

    def __init__(self):
        pass


class JMP:
    arg_name = "JMP"
    base_bin_code = 0x40
    arg_num = 1
    alu_op = False
    append_args = [
        (
            "addr|label",
            0,
            "TWO_ARGA",
            IO(),
            PC(setpc=ENABLE, output=DISABLE, lock=DISABLE),
            DC(address_output=ENABLE, address="datamux"),
            CT(),
            ALU()
        )
    ]

    def __init__(self):
        pass


class PUSH:
    arg_name = "PUSH"
    base_bin_code = 0x50
    arg_num = 1
    alu_op = True
    append_args = [
        (
            "regs",
            0,
            "IO_ONE_ARG",
            IO(rw=OUT, lock=OUT),
            PC(output=DISABLE, lock=ENABLE),
            DC(),
            CT(),
            ALU(rega="arga[3:0]", operate_code="inst[7:0]")
        )
    ]

    def __init__(self):
        pass


class POP:
    arg_name = "POP"
    base_bin_code = 0x51
    arg_num = 1
    alu_op = True
    append_args = [
        (
            "regs",
            0,
            "IO_ONE_ARG",
            IO(rw=IN, lock=IN),
            PC(output=DISABLE, lock=ENABLE),
            DC(),
            CT(),
            ALU(rega="arga[3:0]", operate_code="inst[7:0]")
        )
    ]

    def __init__(self):
        pass


class INT:
    arg_name = "INT"
    base_bin_code = 0x80
    arg_num = 1
    alu_op = False
    append_args = [
        (
            "imdn",
            0,
            "IO_OP",
            IO(),
            PC(setpc=ENABLE),
            DC(),
            CT(soft_int_valid=VALID, soft_int_num="datamux[4:0]"),
            ALU()
        )
    ]

    def __init__(self):
        pass


class SAVEPC:
    arg_name = "SAVEPC"
    base_bin_code = 0x81
    arg_num = 0
    alu_op = True
    next_state = "IO_OP"

    def __init__(self):
        self.io = IO(rw=OUT, lock=OUT),
        self.pc = PC(output=DISABLE, lock=ENABLE),
        self.dc = DC(),
        self.ct = CT(),
        self.alu = ALU(
            direct_io=OUT,
            direct_io_en=ENABLE,
            operate_code="8'hfb"
        )


class RECOPC:
    arg_name = "RECOPC"
    base_bin_code = 0x82
    arg_num = 0
    alu_op = True
    next_state = "IO_OP"

    def __init__(self):
        self.io = IO(),
        self.pc = PC(output=DISABLE, lock=ENABLE),
        self.dc = DC(),
        self.ct = CT(recover_pc=ENABLE),
        self.alu = ALU(
            direct_io=IN,
            direct_io_en=ENABLE,
            operate_code="8'hfc"
        )


instructions_list = [
    NOP(),
    MOV(),
    LOAD(),
    ADD(),
    SUB(),
    AND(),
    OR(),
    NOT(),
    XOR(),
    RAND(),
    ROR(),
    RXOR(),
    LSL(),
    LSR(),
    ASL(),
    ASR(),
    CSL(),
    CSR(),
    INC(),
    DEC(),
    JMP(),
    PUSH(),
    POP(),
    INT(),
    SAVEPC(),
    RECOPC()
]
