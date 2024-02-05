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
    compressed_hex = compressed_domains.hex().upper()
    compressed_text = str(compressed_domains)[12:-2]
    return (compressed_hex, compressed_text)

def format_as_windows(hex_string):
    formatted_string = " ".join([hex_string[i:i+2] for i in range(0, len(hex_string), 2)])
    return formatted_string

def format_as_meraki(hex_string):
    formatted_string = ":".join([hex_string[i:i+2] for i in range(0, len(hex_string), 2)])
    return formatted_string

def format_as_cisco(hex_string):
    formatted_string = ".".join([hex_string[i:i+4] for i in range(0, len(hex_string), 4)])
    return formatted_string

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domain_input", nargs='+', help="Enter the domain name or names as space seperated. ex. google.com apple.com")
    args = parser.parse_args()
    domain_list = ' '.join(args.domain_input)
    print(f'\ndomain search list: {domain_list}\n')
    option_119_hex, option_119_str = convert_domains_to_option_119(args.domain_input)
    meraki_119_string = format_as_meraki(option_119_hex)
    windows_119_string = format_as_windows(option_119_hex)
    cisco_119_string = format_as_cisco(option_119_hex)
    print(f'Meraki: {meraki_119_string}')
    print(f'Cisco: {cisco_119_string}')
    print(f'Windows: {windows_119_string}')
    print(f'systemd-network: SendOption=119:string:{option_119_str}')
    print(f'raw hex: {option_119_hex}')