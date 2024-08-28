from scapy.all import IP, ICMP, sr1
import time

def ping(dest_ip, count=4, ttl=64, packet_size=64, timeout=2):
    try:
        if count <= 0 or ttl <= 0 or packet_size < 0:
            raise ValueError("Invalid value for count, TTL, or packet size.")

        rtt_times = []
        packet_sent = 0
        packet_received = 0

        for i in range(count):
            packet_sent += 1
            pkt = IP(dst=dest_ip, ttl=ttl)/ICMP()/("X"*packet_size)
            start_time = time.time()
            reply = sr1(pkt, verbose=False, timeout=timeout)
            end_time = time.time()
            if reply:
                packet_received += 1
                rtt = (end_time - start_time) * 1000
                rtt_times.append(rtt)
                print(f"{i+1}: Reply from {dest_ip}: bytes={len(reply)} time={round(rtt, 2)}ms TTL={reply.ttl}")
            else:
                print(f"{i+1}: Request timed out.")

        # Calculate statistics
        packet_loss = ((packet_sent - packet_received) / packet_sent) * 100
        if rtt_times:
            avg_rtt = sum(rtt_times) / len(rtt_times)
            min_rtt = min(rtt_times)
            max_rtt = max(rtt_times)
        else:
            avg_rtt = min_rtt = max_rtt = None

        print(f"\n--- {dest_ip} ping statistics ---")
        print(f"{packet_sent} packets transmitted, {packet_received} received, {packet_loss:.2f}% packet loss")
        if avg_rtt is not None:
            print(f"rtt min/avg/max = {round(min_rtt, 2)}/{round(avg_rtt, 2)}/{round(max_rtt, 2)} ms")
        else:
            print("No reply received.")

    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    dest_ip = "8.8.8.8"  # Google's DNS server
    ping(dest_ip, count=4, ttl=64, packet_size=64, timeout=2)
