//Kanvar was here
module cordic
(   
    // ## I/O
    input wire          clk, 
    input wire          init,       // 'go' button for algorithm
    input wire[17:0]    angle_in,   // in radians
    output wire[17:0]   cos,        // in radians
    output wire[17:0]   sin,        // in radians
    output wire[17:0]   angle_out,  // in radians
    output wire         done,       // finished cooking 'ding'

    // ## internal variables (from Python algorithm implementation)
    reg[17:0]       GA;             // angle_in
    reg[17:0]       A;                  // running angle
    reg[17:0]       Delta;
    reg[17:0][1:0]  CS;                 // cos/sin combo variable, 
                                        // matching python modeling
    reg[17:0][1:0]  CS_old;             // cos/sin old var...

    // ## precalculated ROM section...
    reg[15:0]       K; // constant K, just using the 16 fractional bits
    reg[15:0][23]   Delta; // Delta values, 
                            //just using the 16 fractional bits
                            // len=iterations... 23 seems good for now

    // ## misc.
    reg[5:0]        iterations;
    reg             go; // internal 'algorithm running' var
    integer         i;
    

    // ## setting Globals
    iterations <= 17;
    // precalculated value for 2.16 K (steps=17): 0.0.6072529350088871
    // !! The two decimal bits have been cut off, the 16 fractional bits are used
    K = 16'b10011011011101000; // actual value: 0.0.60723876953125  

    always @ (posedge clk) begin
        if (init == 1) begin
            go <= 1; // init needs to be pulled high for one clock cycle to kick off algorithm...
            done <= 0; // clear the done flag...
            // init internal values
            A <= 0;
            C <= 1;
            S <= 0;
            i <= 0;
            // latch input
            GA <= angle_in;
        end

        if (go == 1) begin
            // initialising CS matrix
            if (i == 0) begin
                if (GA >= 0) begin
                    C <= C * K;
                    S <= S * K;
                end else begin
                    C <= C * K;
                    S <= S * -K;
                end
            end

            // store old values
            CS_old <= CS;

            // use precalculated Delta values...
            if (A <= GA) begin
                A <= A + Delta[i];
                CS[0] <= ((CS_old) - (CS_old>>i)) // cos term
                CS[1] <= ((CS_old) + (CS_old>>i)) // sin term
            end else begin
                A <= A - Delta[i];
                CS[0] <= ((CS_old) + (CS_old>>i)) // cos term
                CS[1] <= ((CS_old) - (CS_old>>i)) // sin term
            end

            // increment the index
            i <= i + 1;

            // check are we finished...
            if (i >= iterations) begin
                go <= 0; // step

                // set the done flag...
                done <= 1;
            end
        end
    end
);

endmodule

