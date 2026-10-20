module combo_lock (
    input wire clk,
    input wire areset, //async reset
    input [1:0] btn, //button
    output green_led, //green led state
    output red_led
);
    parameter LOCKED = 0, STEP1 = 1, STEP2 = 2, UNLOCKED = 3, ERROR = 4;
    logic[2:0] state, next_state;

    always_comb begin
        case(state) 
            LOCKED: next_state = (btn == 2'b00) ? STEP1 : ERROR;
            STEP1: next_state = (btn == 2'b01) ? STEP2 : ERROR;
            STEP2: next_state = (btn == 2'b10) ? UNLOCKED : ERROR;
            UNLOCKED: next_state = UNLOCKED;
            ERROR: next_state = LOCKED;
            default: next_state = LOCKED;
        endcase
    end
    //will reset state to locked if async or the next edge after the clock is run
    always_ff @(posedge clk or posedge areset) begin
        if (areset)
            state <= LOCKED;
        else
            state <= next_state;
    end
    assign green_led = (state == UNLOCKED);
    assign red_led = !(state == UNLOCKED);
endmodule
