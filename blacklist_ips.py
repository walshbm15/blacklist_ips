import os
import sys
import csv
import ipaddress
import math

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class Blacklist:
    """
    Uses ipcat's excellent data center list to determine if an ip address if from a know data center.
    https://github.com/client9/ipcat/blob/master/datacenters.csv
    """

    def __init__(self):
        """
        Initialize Blacklist
        """
        self.blacklist_dict = {}
        with open(os.path.join(DIR_PATH, './data/datacenter_ips.csv'),
                  'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                range_start, range_end, _, _ = row
                start_ip = ipaddress.ip_address(range_start)
                end_ip = ipaddress.ip_address(range_end)

                # Hash key, value of start_ip, end_ip and check if IP is between those two values
                self.blacklist_dict[start_ip] = end_ip

            # Make sure the array is sorted so the search can be done faster
            self.start_ip_sorted_array = sorted(self.blacklist_dict.keys())
            self.mid_point_ip_index = math.ceil(len(self.start_ip_sorted_array) / 2)

    def check_ip(self, ip):
        ip_int = ipaddress.ip_address(ip)
        ip_start_key = self.get_blacklist_key(ip_int)
        if ip_start_key <= ip_int <= self.blacklist_dict.get(ip_start_key, 0):
            return True
        else:
            return False

    def get_blacklist_key(self, ip):
        if ip > self.start_ip_sorted_array[self.mid_point_ip_index]:
            # Check list in reverse, cuts iterating list in half is in is in the latter half
            for start_ip in reversed(list(self.start_ip_sorted_array)):
                if start_ip <= ip:
                    return start_ip

        # Iterate list normally
        for i, start_ip in enumerate(self.start_ip_sorted_array):
            if (start_ip > ip and i == 0) or start_ip == ip:
                return start_ip
            elif start_ip > ip:
                return self.start_ip_sorted_array[i - 1]


def main(ip):
    blacklist = Blacklist()
    print(blacklist.check_ip(ip))


if __name__ == "__main__":
    # Expects ip arg when called from the command line
    main(sys.argv[1])
