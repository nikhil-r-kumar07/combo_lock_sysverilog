SIM ?= icarus
TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES += $(PWD)/combo_lock.sv
TOPLEVEL = combo_lock
MODULE = test_combo_lock
include @(shell cocotb-config --makefiles)/Makefile.SIM
