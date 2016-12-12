import argparse
import sys
import logging

from util import get_ip_address
from aircast import start_aircast

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--port', type=int, default=8000,
                        help='Port on which the AirCast web server will be started')
    parser.add_argument('--shairport_port', type=int, default=5000,
                        help='Port on which the Shairport Sync Airplay web server will be started')    
    parser.add_argument('--iface', type=str, default="eth0",
                        help='Interface on which the AirCast web server will be exposed')
    parser.add_argument('--chromecast', type=str, default=None,
                        help='Chromecast name to connect to when there are multiple chromecasts on the network')

    args = parser.parse_args()

    start_aircast(get_ip_address(args.iface), args.port, args.chromecast)
