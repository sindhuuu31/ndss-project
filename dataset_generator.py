import csv
import random

def generate_dataset(filename="ndss_traffic_dataset.csv", num_samples=2000):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["packet_count", "packet_size", "entropy", "label"])
        
        for _ in range(num_samples):
            # Label 0: Normal Traffic, Label 1: DDoS Attack
            is_attack = random.random() < 0.3 # 30% attack traffic
            
            if is_attack:
                # DDoS characteristics: high packet count, fixed/identical packet sizes, low entropy (or very high if random payload)
                packet_count = random.randint(8000, 20000)
                packet_size = random.choice([64, 128, 512]) # attackers often use fixed sizes
                entropy = random.uniform(0.1, 2.5) # mostly repetitive data, low entropy
                label = 1
            else:
                # Normal web browsing: reasonable counts, varying sizes, standard entropy
                packet_count = random.randint(100, 1500)
                packet_size = random.randint(64, 1500)
                entropy = random.uniform(3.0, 7.8) # Encrypted normal web traffic is high entropy
                label = 0
                
            writer.writerow([packet_count, packet_size, round(entropy, 4), label])
            
    print(f"Dataset {filename} generated with {num_samples} samples.")

if __name__ == "__main__":
    generate_dataset()
