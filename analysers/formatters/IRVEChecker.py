import re


###########################################################################

def remove_trailing_zeros(input_string):
    """
    Removes dot and zeros at the end of a floating number typed in string
    """
    return str(input_string).replace('.00', '').replace('.0', '')


def is_float(str):
    """
    Returns True if the input string can be converted to a float, False otherwise.
    """
    pattern = r"^-?\d+(\.\d+)?$"
    return bool(re.match(pattern, str))


class IRVE_checker():

    def socket_output_find_correspondances(power: str):
        """
           convert the number of Watts to kiloWatts
           output example:
           - "400 kW"
           - "7 kW"
           - "50.6 kW"
        """
        power = power.replace(',', '.')

        # remove extremely high values or the ones containing letters
        max_output_kw = 1999
        detection_watts = 2000
        # we take an upper limit of 400 kW
        max_kw = 401

        # values under the max expected kW are used as is,
        # upper values are Watts, which we should divide by 1000 to get kW

        print("input: ", power)
        if not power:
            return ''
        if re.search(r"[a-zA-Z]+", power):
            print("The string contains letters.")
            return ''

        if not is_float(power) and int(power) > detection_watts:
            power = int(power) / 1000

        if not is_float(power) or float(power) < 1:
            return ''

        if float(power) < max_output_kw:
            return '{0} kW'.format(remove_trailing_zeros(str(round(float(power), 2))))

        else:
            if float(power) > (max_kw * 1000):
                return ''

        # clean the values of power
        cleanedPower = remove_trailing_zeros(power)
        converted_power = (float(cleanedPower)) or 0

        if "." in str(converted_power):
            # print("contient une partie décimale")
            if '.0' in str(converted_power) or '.00' in str(converted_power):
                str_power = str(converted_power).replace('.0', '')
                converted_power = int(str_power)

        print('converted_power', converted_power)
        if converted_power > detection_watts and converted_power < (max_kw * 1000):
            converted_power = remove_trailing_zeros(converted_power / 1000)
            print('power is in watt, converted gives:', converted_power)
            if float(converted_power) > max_output_kw:
                return '';
            else:
                if float(converted_power) > max_kw:
                    return '{0} kW'.format(remove_trailing_zeros(converted_power / 1000))
        else:
            converted_power = converted_power / 1000

        if float(converted_power) > max_kw:
            return ''

        if converted_power != 0:
            return '{0} kW'.format(converted_power)
        else:
            return ''
