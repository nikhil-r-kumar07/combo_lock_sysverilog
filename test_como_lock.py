import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

async def reset_dut(dut):
    dut.areset.value = 1
    dut.btn.value = 0b11
    await Timer(20, units="ns")
    dut.areset.value = 0
    await RisingEdge(dut.clk)

@cocotb.test()
async def test_correct_sequence(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units = "ns").start())
    await reset_dut(dut)
    assert dut.green_led.value == 0, "Should start locked"
    for digit in [0b00, 0b01, 0b10]:
        dut.btn.value = digit
        await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    assert dut.green_led.value == 1, \
        f"Expected unlocked, green_led={dut.green_led.value}"

@cocotb.test()
async def test_wrong_digit(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units = "ns").start())
    await reset_dut(dut)
    dut.btn.value = 0b00
    await RisingEdge(dut.clk)
    dut.btn.value = 0b11
    await RisingEdge(dut.clk) // Error
    await RisingEdge(dut.clk) // Locked
    assert dut.green_led.value == 0, "Should not be unlocked"

@cocotb.test()
async def test_reset_mid_sequence(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units = "ns").start())
    await reset_dut(dut)
    dut.btn.value = 0b00
    await RisingEdge(dut.clk)
    dut.areset.value = 1
    await Timer(1, units="ns")
    assert dut.green_led.value == 0, "Reset should lock immediately"
    dut.areset.value = 0
    await RisingEdge(dut.clk)
