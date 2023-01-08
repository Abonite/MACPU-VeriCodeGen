from instructions import instructions_list

instrctions_vh_file = "instructions.vh"
alu_operate_codes_vh_file = "alu_opc.vh"
decoder_task_file = "decoder_task.txt"
decoder_one_arg_exec_file = "decoder_oae.txt"
decoder_two_argb_exec_file = "decoder_tae.txt"
decoder_io_op_exec_file = "decoder_io.txt"

instructions = []
alu_operate_code = []
alu_operate_code_record = []
decoder_next_state_task = []
decoder_one_arg_exec = ["ONE_ARG: begin\n\tcase (inst)\n"]
decoder_two_argb_exec = ["TWO_ARGB: begin\n\tcase (inst)\n"]
decoder_io_op_exec = ["IO_OP: begin\n\tcase (inst)\n"]

for inst in instructions_list:
    arg_name = inst.arg_name
    base_bin_code = inst.base_bin_code
    arg_num = inst.arg_num
    is_alu_op = inst.alu_op

    if arg_num == 2:
        append_args = inst.append_args
        if len(append_args) >= 1:
            for argatype, argbtype, append_code, next_state, io, pc, dc, ct, alu in append_args:
                append_inst_name = ""
                if len(append_args) > 1:
                    append_inst_name = \
                        "_" + argatype[0].upper() + argbtype[0].upper()
                real_op_code = base_bin_code + append_code
                instructions.append(
                    "".join([
                        f"`define\t{arg_name}{append_inst_name}".ljust(
                            20,
                            " "
                        ),
                        f"16'h{hex(real_op_code)[2:]}\n"
                    ])
                )

                decoder_next_state_task.append(
                    "".join([
                        f"`{arg_name}{append_inst_name}:".ljust(10, " "),
                        f"next_state\t=\t{next_state};\n"
                    ])
                )

                decoder_op = "".join([
                        f"\t\t`{arg_name}{append_inst_name}: begin\n",
                        f"\t\t\tio_control_code = {io.io_control_code()};\n",
                        f"\t\t\tpc_control_code = {pc.pc_control_code()};\n",
                        f"\t\t\tdc_control_code = {dc.dc_control_code()};\n",
                        f"\t\t\tct_control_code = {ct.ct_control_code()};\n",
                        f"\t\t\talu_control_code = {alu.alu_control_code()};\n",
                        f"\t\t\taddr = {dc.get_dc_address()};\n",
                        f"\t\t\tdata_alu = {dc.get_alu_data()};\n",
                        "\t\tend\n"
                    ])

                if next_state == "ONE_ARG":
                    decoder_one_arg_exec.append(decoder_op)
                elif next_state == "TWO_ARGA":
                    decoder_two_argb_exec.append(decoder_op)
                elif next_state.startswith("IO"):
                    decoder_io_op_exec.append(decoder_op)

                if is_alu_op:
                    if real_op_code & 0b1111_1111 in alu_operate_code_record:
                        print(f"[ERROR] alu opcode duplication: {arg_name}{append_inst_name}")
                    else:
                        alu_operate_code_record.append(
                            real_op_code & 0b1111_1111
                        )
                        alu_operate_code.append(
                            "".join([
                                f"`define\t{arg_name}{append_inst_name}".ljust(
                                    20,
                                    " "
                                ),
                                f"8'b{bin(real_op_code & 0b1111_1111)[2:]}\n"
                            ])
                        )
    elif arg_num == 1:
        append_args = inst.append_args
        if len(append_args) >= 1:
            for argtype, append_code, next_state, io, pc, dc, ct, alu in append_args:
                append_inst_name = ""
                if len(append_args) > 1:
                    append_inst_name = "_" + argtype[0].upper()
                real_op_code = base_bin_code + append_code
                instructions.append(
                    "".join([
                        f"`define\t{arg_name}{append_inst_name}".ljust(
                            20,
                            " "
                        ),
                        f"16'h{hex(real_op_code)[2:]}\n"
                    ])
                )

                decoder_next_state_task.append(
                    "".join([
                        f"`{arg_name}{append_inst_name}:".ljust(10, " "),
                        f"next_state\t=\t{next_state};\n"
                    ])
                )

                decoder_op = "".join([
                        f"\t\t`{arg_name}{append_inst_name}: begin\n",
                        f"\t\t\tio_control_code = {io.io_control_code()};\n",
                        f"\t\t\tpc_control_code = {pc.pc_control_code()};\n",
                        f"\t\t\tdc_control_code = {dc.dc_control_code()};\n",
                        f"\t\t\tct_control_code = {ct.ct_control_code()};\n",
                        f"\t\t\talu_control_code = {alu.alu_control_code()};\n",
                        f"\t\t\taddr = {dc.get_dc_address()};\n",
                        f"\t\t\tdata_alu = {dc.get_alu_data()};\n",
                        "\t\tend\n"
                    ])

                if next_state == "ONE_ARG":
                    decoder_one_arg_exec.append(decoder_op)
                elif next_state == "TWO_ARGA":
                    decoder_two_argb_exec.append(decoder_op)
                elif next_state.startswith("IO"):
                    decoder_io_op_exec.append(decoder_op)

                if is_alu_op:
                    if real_op_code & 0b1111_1111 in alu_operate_code_record:
                        print(f"[ERROR] alu opcode duplication: {arg_name}{append_inst_name}")
                    else:
                        alu_operate_code_record.append(
                            real_op_code & 0b1111_1111
                        )
                        alu_operate_code.append(
                            "".join([
                                f"`define\t{arg_name}".ljust(20, " "),
                                f"8'b{bin(real_op_code & 0b1111_1111)[2:]}\n"
                            ])
                        )
    elif arg_num == 0:
        try:
            io = inst.io.io_control_code()
        except AttributeError:
            io = inst.io[0].io_control_code()

        try:
            pc = inst.pc.pc_control_code()
        except AttributeError:
            pc = inst.pc[0].pc_control_code()

        try:
            dc = inst.dc.dc_control_code()
            dc_addr = inst.dc.get_dc_address()
            dc_data = inst.dc.get_alu_data()
        except AttributeError:
            dc = inst.dc[0].dc_control_code()
            dc_addr = inst.dc[0].get_dc_address()
            dc_data = inst.dc[0].get_alu_data()

        try:
            ct = inst.ct.ct_control_code()
        except AttributeError:
            ct = inst.ct[0].ct_control_code()

        try:
            alu = inst.alu.alu_control_code()
        except AttributeError:
            alu = inst.alu[0].alu_control_code()

        next_state = inst.next_state

        instructions.append(
            "".join([
                f"`define\t{arg_name}".ljust(20, " "),
                f"16'h{hex(base_bin_code)[2:]}\n"
            ])
        )

        decoder_next_state_task.append(
            "".join([
                f"`{arg_name}:".ljust(10, " "),
                "next_state\t=\tINST;\n"
            ])
        )

        decoder_op = "".join([
                f"\t\t`{arg_name}: begin\n",
                f"\t\t\tio_control_code = {io};\n",
                f"\t\t\tpc_control_code = {pc};\n",
                f"\t\t\tdc_control_code = {dc};\n",
                f"\t\t\tct_control_code = {ct};\n",
                f"\t\t\talu_control_code = {alu};\n",
                f"\t\t\taddr = {dc_addr};\n",
                f"\t\t\tdata_alu = {dc_data};\n",
                "\t\tend\n"
            ])

        if next_state == "ONE_ARG":
            decoder_one_arg_exec.append(decoder_op)
        elif next_state == "TWO_ARGA":
            decoder_two_argb_exec.append(decoder_op)
        elif next_state.startswith("IO"):
            decoder_io_op_exec.append(decoder_op)

        if is_alu_op:
            if base_bin_code & 0b1111_1111 in alu_operate_code_record:
                print(f"[ERROR] alu opcode duplication: {arg_name}{append_inst_name}")
            else:
                alu_operate_code_record.append(
                    real_op_code & 0b1111_1111
                )
                alu_operate_code.append(
                    "".join([
                        f"`define\t{arg_name}".ljust(20, " "),
                        f"8'b{bin(real_op_code & 0b1111_1111)[2:]}\n"
                    ])
                )

decoder_one_arg_exec.append("\tendcase\nend")
decoder_two_argb_exec.append("\tendcase\nend")
decoder_io_op_exec.append("\tendcase\nend")

with open(instrctions_vh_file, "a+") as ivf:
    ivf.seek(0)
    ivf.truncate()
    ivf.seek(0)
    ivf.writelines(instructions)

with open(alu_operate_codes_vh_file, "a+") as aocvf:
    aocvf.seek(0)
    aocvf.truncate()
    aocvf.seek(0)
    aocvf.writelines(alu_operate_code)

with open(decoder_task_file, "a+") as do:
    do.seek(0)
    do.truncate()
    do.seek(0)
    do.writelines(decoder_next_state_task)

with open(decoder_one_arg_exec_file, "a+") as doae:
    doae.seek(0)
    doae.truncate()
    doae.seek(0)
    doae.writelines(decoder_one_arg_exec)

with open(decoder_two_argb_exec_file, "a+") as dtae:
    dtae.seek(0)
    dtae.truncate()
    dtae.seek(0)
    dtae.writelines(decoder_two_argb_exec)

with open(decoder_io_op_exec_file, "a+") as dioef:
    dioef.seek(0)
    dioef.truncate()
    dioef.seek(0)
    dioef.writelines(decoder_io_op_exec)
