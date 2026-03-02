import math
import numpy as np

def calc_fixed_point(num, dec_bits=2,float_bits=16, print_en=False):
    ## given a floating point number calculate the 2.16 fixed point representation of it...

    # get decimal part be flooring the number...
    decimal = math.floor(num)
    if print_en:
        print(f'Decimal: {decimal}')

    # we have 2 bits to store this, so if the decimal part is greater than 3 throw an error
    if decimal > dec_bits:
        raise ValueError(f"decimal part greater than {dec_bits}")

    # take the original number and subtract the decimal part off it
    fractional_original = num - decimal
    if print_en:
        print(f'Fractional original: {fractional_original}\n')

    # iteratively approximate it using 16 bits...
    # use simple list to store bits...
    # 2^(-1), 2^(-2)... 2^(-16)
    fractional = 0
    bits = np.zeros(float_bits+1, dtype=int)
    for i in range(1, float_bits+1):

        # set the bit
        if fractional <= fractional_original:
            fractional += 2 ** (-i)
            bits[i-1] = 1

            # check if we go past the num
            if fractional > fractional_original:
                # unset the bit
                fractional -= 2 ** (-i)
                bits[i-1] = 0

        if print_en:
            print(f'Fractional ({i} bit): {fractional}')
            print(f'Bits: {bits}')
            print('')

    # check we are correct
    test = decimal
    for i in range(1,float_bits+1):
        test += bits[i-1]*2**(-i)

    bits_string = ''
    for bit in bits:
        bits_string += format(bit,'b')

    if print_en:
        print(f'Original:\t{decimal + fractional_original}')
        print(f'Test:\t\t{test}\n')
        print(f'Final fixed point representation:\n{format(decimal, '02b')}.{bits_string}'
              f'\n{format(decimal, '02b')}{bits_string}')

    return f'{format(decimal, '02b')}{bits_string}'

calc_fixed_point(0.6072529350088871, print_en=True)

