#!/usr/bin/env python3
#
# take in a domain name or space seperated list of domain names and convert to dhcp option 119
#
import argparse

def convert_domains_to_option_119(domains):
    compressed_domains = bytearray()
    pointers = {}
    for domain in domains:
        parts = domain.lower().split('.')
        for i in range(len(parts)):
            suffix = '.'.join(parts[i:])
            if suffix in pointers:
                pointer = pointers[suffix]
                compressed_domains.extend([0xc0, 0x00 | pointer])
                break
            else:
                pointers[suffix] = len(compressed_domains)
                compressed_domains.extend([len(parts[i]), *[ord(char) for char in parts[i]]])
        else:
             compressed_domains.append(0x00)
    return (compressed_domains.hex().upper())

def format_as_windows(hex_string):
    formatted_string = " ".join([hex_string[i:i+2] for i in range(0, len(hex_string), 2)])
    return formatted_string

def format_as_meraki(hex_string):
    formatted_string = ":".join([hex_string[i:i+2] for i in range(0, len(hex_string), 2)])
    return formatted_string

def format_as_cisco(hex_string):
    formatted_string = ".".join([hex_string[i:i+4] for i in range(0, len(hex_string), 4)])
    return formatted_string

def format_as_systemd(hex_string):
    byte_array = bytearray.fromhex(hex_string)
    decoded_text = ""
    for byte in byte_array[0:]:
        if byte < 32 or byte == 127:
            decoded_text += f'\\x{byte:02x}'
        else:
            try:
                decoded_text += byte.to_bytes(1, 'little').decode('utf-8')
            except UnicodeDecodeError:
                decoded_text += f'\\x{byte:02x}'
    return(decoded_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domain_input", nargs='+', help="Enter the domain name or names as space seperated. ex. google.com apple.com")
    args = parser.parse_args()
    domain_list = ' '.join(args.domain_input)
    print(f'\ndomain search list: {domain_list}\n')
    option_119_hex = convert_domains_to_option_119(args.domain_input)

    print(f'Meraki: {format_as_meraki(option_119_hex)}')
    print(f'Cisco: {format_as_cisco(option_119_hex)}')
    print(f'Windows: {format_as_windows(option_119_hex)}')
    print(f'systemd-network: SendOption=119:string:{format_as_systemd(option_119_hex)}')
    print(f'raw hex: {option_119_hex}')
