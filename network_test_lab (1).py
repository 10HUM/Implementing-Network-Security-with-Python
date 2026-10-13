#!/usr/bin/env python3

# Native Python Modules
import ctypes
import os
import socket
import sys

# Additional Python Modules
import ping3
import psutil


def check_local_listeners():
    """
    Identify and display processes listening on open ports.

    Uses psutil to retrieve all active network connections,
    filters for those in the LISTEN state, and displays the
    process name, PID, listening IP address, and port number
    in a clean, formatted table. Requires elevated permissions
    to retrieve details for all system processes.
    """
    print(f"{'PROCESS':<20} {'PID':<6} {'IP':<16} {'PORT':<6}")
    for connection in psutil.net_connections():
        # Skip connections that are not actively listening
        if connection.status != "LISTEN":
            continue
        # Skip connections with no associated process ID
        if connection.pid is None:
            continue
        # Extract connection details
        process_id = connection.pid
        listen_ip = connection.laddr.ip
        listen_port = connection.laddr.port
        # Resolve the process name from its PID
        process_name = psutil.Process(process_id).name()
        # Print the row in a formatted, aligned table
        print(
            f"{process_name:<20} {process_id:<6} "
            f"{listen_ip:<16} {listen_port:<6}"
        )


def check_permissions():
    """
    Verify the script is running with administrative privileges.

    Checks for root access on POSIX systems (Linux/macOS) using
    os.getuid(), and checks for Administrator rights on Windows
    using ctypes. Prints an ERROR and USAGE message then exits
    with code 1 if sufficient privileges are not detected.
    """
    if os.name == "posix":
        # On Linux/macOS, root has a user ID of 0
        if os.getuid() != 0:
            print("ERROR: Administrative privileges are required.")
            print("USAGE: sudo python3.12 network_test_lab.py")
            exit(1)
    elif os.name == "nt":
        # On Windows, use the ctypes shell API to check admin status
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except AttributeError:
            # ctypes unavailable — conservatively assume not admin
            is_admin = False
        if not is_admin:
            print("ERROR: Administrative privileges are required.")
            print("USAGE: Run as Administrator or use an elevated Command Prompt.")
            exit(1)


def dns_ping_test():
    """
    Test DNS resolution and connectivity to a known domain.

    Uses ping3 to send an ICMP echo request to flatironschool.com,
    verifying both that the system can resolve the domain name via
    DNS and that the resolved host is reachable over the network.
    A successful response confirms end-to-end DNS functionality.
    """
    # Target domain used to verify DNS resolution capability
    target = "flatironschool.com"
    response = ping3.ping(target)
    if response is not None:
        # A non-None return value means the ping succeeded
        print(" [✓] DNS Check Passed")
    else:
        print(" [x] DNS Check was Unsuccessful")


def get_local_ips():
    """
    Display all active network interfaces with IPv4 and IPv6 addresses.

    Uses psutil to retrieve all available network interfaces and
    iterates through their associated addresses. Filters using the
    socket library to display both AF_INET (IPv4) and AF_INET6 (IPv6)
    address families, providing a complete picture of the machine's
    network configuration for audit purposes.
    """
    # Retrieve a dictionary of interface names to address lists
    interfaces = psutil.net_if_addrs()
    for interface in interfaces:
        print("Interface:", interface)
        for snicaddr in interfaces[interface]:
            # Check for and display IPv4 addresses
            if snicaddr.family == socket.AF_INET:
                print(f"  - IPv4: {snicaddr.address}")
            # Check for and display IPv6 addresses
            elif snicaddr.family == socket.AF_INET6:
                print(f"  - IPv6: {snicaddr.address}")


def ping_test():
    """
    Test network connectivity by pinging a known external IP address.

    Uses ping3 to send an ICMP echo request to Google's public DNS
    server at 8.8.8.8. This test verifies basic internet connectivity
    without relying on DNS resolution, isolating raw IP-level
    reachability as a distinct audit step.
    """
    # Google's public DNS server — globally reliable and always available
    target = "8.8.8.8"
    response = ping3.ping(target)
    if response is not None:
        print(" [✓] Network Connectivity Check Passed")
    else:
        print(" [x] Network Connectivity Check was Unsuccessful")


def main():
    """
    Orchestrate the full network auditing workflow.

    Verifies administrative permissions first, then sequentially
    collects network interface information (IPv4 and IPv6), tests
    internet connectivity and DNS resolution, and audits all
    processes currently listening on open ports. Designed to support
    PCI-DSS risk assessment requirements for e-commerce environments.
    """
    # Gate the entire script on admin privileges — exits with code 1 if unmet
    check_permissions()

    print("Script is running with sufficient permissions.")

    print("=" * 40)
    print("Network Interface Information:")
    print("=" * 40)
    get_local_ips()

    print("=" * 40)
    print("Connectivity Tests:")
    print("=" * 40)
    ping_test()
    dns_ping_test()

    print("=" * 40)
    print("Listening Ports:")
    print("=" * 40)
    check_local_listeners()


# Entry point — only runs main() when script is executed directly,
# not when imported as a module (e.g., by CodeGrade's test runner)
if __name__ == "__main__":
    main()