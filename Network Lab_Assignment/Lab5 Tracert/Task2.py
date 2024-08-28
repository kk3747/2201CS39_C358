from scapy.all import IP, ICMP, sr1, conf
import time

def tracert(dest_ip, max_ttl=30, packet_size=64, timeout=2, src_ip=None, num_pings=3, delay=1, output_file=None):
    try:
        # Set the source IP if specified
        if src_ip:
            conf.src = src_ip
        
        # Prepare to save output if specified
        if output_file:
            f = open(output_file, 'w')
        else:
            f = None  # Set f to None if no output file is specified

        print(f"Tracing route to {dest_ip} over a maximum of {max_ttl} hops:")
        if f:
            f.write(f"Tracing route to {dest_ip} over a maximum of {max_ttl} hops:\n")

        for ttl in range(1, max_ttl + 1):
            rtt_times = []
            packet_sent = 0
            packet_received = 0

            for i in range(num_pings):
                packet_sent += 1
                pkt = IP(dst=dest_ip, ttl=ttl)/ICMP()/("X"*packet_size)
                start_time = time.time()
                reply = sr1(pkt, verbose=False, timeout=timeout)
                end_time = time.time()

                if reply:
                    packet_received += 1
                    rtt = (end_time - start_time) * 1000  # RTT in milliseconds
                    rtt_times.append(rtt)
                    print(f"{ttl}\t{reply.src}\t{round(rtt, 2)} ms")
                    if f:
                        f.write(f"{ttl}\t{reply.src}\t{round(rtt, 2)} ms\n")
                    if reply.src == dest_ip:
                        print("Trace complete.")
                        if f:
                            f.write("Trace complete.\n")
                        break
                else:
                    print(f"{ttl}\t*\tRequest timed out.")
                    if f:
                        f.write(f"{ttl}\t*\tRequest timed out.\n")

                time.sleep(delay)

            if reply and reply.src == dest_ip:
                break

            packet_loss = ((packet_sent - packet_received) / packet_sent) * 100
            if rtt_times:
                avg_rtt = sum(rtt_times) / len(rtt_times)
                min_rtt = min(rtt_times)
                max_rtt = max(rtt_times)
            else:
                avg_rtt = min_rtt = max_rtt = None

            print(f"Hop {ttl}: Sent={packet_sent}, Received={packet_received}, Loss={packet_loss:.2f}%, min/avg/max RTT = {min_rtt}/{avg_rtt}/{max_rtt} ms")
            if f:
                f.write(f"Hop {ttl}: Sent={packet_sent}, Received={packet_received}, Loss={packet_loss:.2f}%, min/avg/max RTT = {min_rtt}/{avg_rtt}/{max_rtt} ms\n")

        if f:
            f.close()

    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    tracert("google.com", num_pings=3, delay=1, output_file="tracert_output.txt")
