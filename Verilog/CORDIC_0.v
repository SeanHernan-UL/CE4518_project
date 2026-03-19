// ## CE4518 Project Work: CORDIC
// ## Group members (ID):  Kanvar Murray (22374698),
// ##                      Seán Hernan (22348948)

`timescale 1ns / 1ps
`default_nettype none

//Kanvar was here
module cordic
(  
    // ## I/O
    input wire          clk,
    input wire          init,               // 'go' button for algorithm
    input wire[17:0]    angle_in,           // in radians
    output reg[17:0]    cos,                // in radians
    output reg[17:0]    sin,                // in radians
    output reg[17:0]    angle_out,          // in radians
    output reg          done                // finished cooking 'ding'
);

    // ## internal variables (from Python algorithm implementation)
    reg signed[17:0]           GA;                 // angle_in
    reg signed[17:0]           A;                  // running angle
    reg signed[17:0]           C;                  // cos
    reg signed[17:0]           S;                  // sin
    reg signed[17:0]           C_old;              // cos old
    reg signed[17:0]           S_old;              // sin old

    // ## precalculated ROM section...
    reg signed[17:0]           K;                  // constant K, just using the 
                                            // 16 fractional bits
    reg[17:0]           Delta [0:17];       // Delta values,

    // ## misc.
    reg[5:0]            steps;
    reg                 go;                 // internal 'algorithm running' var
    reg[5:0]            i;

    reg                 if_less;
   
initial begin
    // ## setting Globals
    steps = 5'd17;

    // precalculated value for 2.16 K (steps=17): 0.6072529350324458
    K = 18'b001001101101110100; // actual value: 0.60723876953125

    // Delta[0], wrapped into A, just check sign of GA...
    Delta[1] = 18'b000111011010110001; // 0.46364761 rad
    Delta[2] = 18'b000011111010110110; // 0.24497866 rad
    Delta[3] = 18'b000001111111010101; // 0.12435499 rad
    Delta[4] = 18'b000000111111111010; // 0.06241881 rad
    Delta[5] = 18'b000000011111111111; // 0.03123983 rad
    Delta[6] = 18'b000000001111111111; // 0.01562373 rad
    Delta[7] = 18'b000000000111111111; // 0.00781234 rad
    Delta[8] = 18'b000000000011111111; // 0.00390623 rad
    Delta[9] = 18'b000000000001111111; // 0.00195312 rad
    Delta[10] = 18'b000000000000111111; // 0.00097656 rad
    Delta[11] = 18'b000000000000011111; // 0.00048828 rad
    Delta[12] = 18'b000000000000001111; // 0.00024414 rad
    Delta[13] = 18'b000000000000000111; // 0.00012207 rad
    Delta[14] = 18'b000000000000000100; // 6.104e-05 rad
    Delta[15] = 18'b000000000000000010; // 3.052e-05 rad
    Delta[16] = 18'b000000000000000001; // 1.526e-05 rad
    // padding with dummy, so A doesn't go to XXXs on last clock when setting outputs
    Delta[17] = 18'b000000000000000000; 
end

always @ (posedge clk) begin
    if (init == 1) begin
        go <= 1; // init needs to be pulled high for one clock cycle to kick off algorithm...
        done <= 0; // clear the done flag...
        i <= 1; // wrapped the 0 step into K, start at 1
        GA <= angle_in; // latch input

        // wipe output values
        cos <= 0;
        sin <= 0;
        angle_out <= 0;

        // get A value and init C and S
        // since init, GA isn't available yet... use raw angle_in
        if (!(angle_in >> 17)) begin // if 'GA' is positive value
            A <=  (18'b001100100100001111); // 45 degrees in radians
            C <= K;
            S <= K;
        end else begin
            A <=  (18'b110011011011110001); // -45 degrees in radians (2's complement)
            C <= K;
            S <= ~K + 1; // two's complement for negative
        end
    end

    if (go == 1) begin
        // increment the index
        i <= i + 1; // might as well do it here

        // use precalculated Delta values...
        // handle comparison in two's complement
        if (A<=GA) begin // seems to be better than <=, do full tests with both...
            A <= A + Delta[i];
            C <= (C + (~(S>>>i)+1)); // cos term
            S <= ((C>>>i) + S); // sin term
            if_less = 1;
        end else begin
            A <= A - Delta[i];
            C <= (C + (S>>>i)); // cos term
            S <= ((~(C>>>i)+1) + S); // sin term
            if_less = 0;
        end

        // check are we finished...
        if (i >= steps) begin
            // set output values
            cos <= C;
            sin <= S;
            angle_out <= A;

            go <= 0; // stop
            done <= 1; // set the done flag...
        end
    end
end

endmodule