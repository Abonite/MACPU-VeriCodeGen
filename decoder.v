`NOP:     next_state	=	INST;
`MOV_AR:  next_state	=	IO_ARGA;
`MOV_RR:  next_state	=	TWO_ARGA;
`MOV_RA:  next_state	=	IO_ARGA;
`LOAD:    next_state	=	TWO_ARGA;
`ADD_RR:  next_state	=	TWO_ARGA;
`ADD_RI:  next_state	=	TWO_ARGA;
`SUB_RR:  next_state	=	TWO_ARGA;
`SUB_RI:  next_state	=	TWO_ARGA;
`AND_RR:  next_state	=	TWO_ARGA;
`AND_RI:  next_state	=	TWO_ARGA;
`OR_RR:   next_state	=	TWO_ARGA;
`OR_RI:   next_state	=	TWO_ARGA;
`NOT_RR:  next_state	=	TWO_ARGA;
`NOT_RI:  next_state	=	TWO_ARGA;
`XOR_RR:  next_state	=	TWO_ARGA;
`XOR_RI:  next_state	=	TWO_ARGA;
`RAND_R:  next_state	=	TWO_ARGA;
`RAND_I:  next_state	=	TWO_ARGA;
`ROR_R:   next_state	=	TWO_ARGA;
`ROR_I:   next_state	=	TWO_ARGA;
`RXOR_R:  next_state	=	TWO_ARGA;
`RXOR_I:  next_state	=	TWO_ARGA;
`LSL_R:   next_state	=	ONE_ARG;
`LSL_I:   next_state	=	TWO_ARGA;
`LSR_R:   next_state	=	ONE_ARG;
`LSR_I:   next_state	=	TWO_ARGA;
`ASL_R:   next_state	=	ONE_ARG;
`ASL_I:   next_state	=	TWO_ARGA;
`ASR_R:   next_state	=	ONE_ARG;
`ASR_I:   next_state	=	TWO_ARGA;
`CSL_R:   next_state	=	ONE_ARG;
`CSL_I:   next_state	=	TWO_ARGA;
`CSR_R:   next_state	=	ONE_ARG;
`CSR_I:   next_state	=	TWO_ARGA;
`INC:     next_state	=	TWO_ARGA;
`DEC:     next_state	=	TWO_ARGA;
`JMP:     next_state	=	TWO_ARGA;
`PUSH:    next_state	=	IO_ONE_ARG;
`POP:     next_state	=	IO_ONE_ARG;
`INT:     next_state	=	ONE_ARG;
`SAVEPC:  next_state	=	INST;
`RECOPC:  next_state	=	INST;



`NOP: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {8'b0, 4'h0, 4'h0, 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`MOV_AR: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b100;
	dc_control_code = 4'b0100;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, argb[3:0], 3'b010};
	addr = arga;
	data_alu = 16'h0;
end


`MOV_RR: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], argb[3:0], arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`MOV_RA: begin
	io_control_code = 2'b11;
	pc_control_code = 3'b100;
	dc_control_code = 4'b0100;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, arga[3:0], 3'b011};
	addr = argb;
	data_alu = 16'h0;
end


`LOAD: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, datamux[3:0], 3'b010};
	addr = 16'b0;
	data_alu = arga;
end


`ADD_RR: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], datamux[3:0], arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`ADD_RI: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h8, arga[3:0], 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


`SUB_RR: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], datamux[3:0], arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`SUB_RI: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h8, arga[3:0], 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


`AND_RR: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], datamux[3:0], arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`AND_RI: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h8, arga[3:0], 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


`OR_RR: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], datamux[3:0], arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`OR_RI: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h8, arga[3:0], 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


`NOT_RR: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], datamux[3:0], arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`NOT_RI: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h8, arga[3:0], 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


`XOR_RR: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], datamux[3:0], arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`XOR_RI: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h8, arga[3:0], 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


`RAND_R: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`RAND_I: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, 4'h8, 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


`ROR_R: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`ROR_I: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, 4'h8, 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


`RXOR_R: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`RXOR_I: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, 4'h8, 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


`LSL_R: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`LSL_I: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, 4'h8, 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


`LSR_R: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`LSR_I: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, 4'h8, 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


`ASL_R: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`ASL_I: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, 4'h8, 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


`ASR_R: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`ASR_I: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, 4'h8, 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


`CSL_R: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`CSL_I: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, 4'h8, 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


`CSR_R: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`CSR_I: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, 4'h8, 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


`INC: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`DEC: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b010;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`JMP: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b001;
	dc_control_code = 4'b0110;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {8'b0, 4'h0, 4'h0, 3'b000};
	addr = datamux;
	data_alu = 16'h0;
end


`PUSH: begin
	io_control_code = 2'b11;
	pc_control_code = 3'b100;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`POP: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b100;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {inst[7:0], 4'h0, arga[3:0], 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`INT: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b011;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, datamux[4:0], 1'b1, 2'b00, 4'b0000};
	alu_control_code = {8'b0, 4'h0, 4'h0, 3'b000};
	addr = 16'b0;
	data_alu = 16'h0;
end


`SAVEPC: begin
	io_control_code = 2'b11;
	pc_control_code = 3'b100;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b0, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {8'hfb, 4'h0, 4'h0, 3'b011};
	addr = 16'b0;
	data_alu = 16'h0;
end


`RECOPC: begin
	io_control_code = 2'b00;
	pc_control_code = 3'b100;
	dc_control_code = 4'b0010;
	ct_control_code = {1'b1, 5'b0, 1'b0, 2'b00, 4'b0000};
	alu_control_code = {8'hfc, 4'h0, 4'h0, 3'b010};
	addr = 16'b0;
	data_alu = 16'h0;
end


