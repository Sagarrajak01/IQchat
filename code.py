# Define the name mapping
name_map = {
    "Sagar": "Alice",
    "Hasrat": "Carol",
    "Roshan": "Bob",
    "Rishikesh": "Cave",
    "Abhishek": "Dev",
    "Vishal": "Frank"
}

# Input and output file paths
input_file = "chat.txt"
output_file = "chat_with_new_names.txt"

# Read the file and replace names
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    for old_name, new_name in name_map.items():
        # Only replace name at the start of the message after timestamp
        if f"- {old_name}:" in line:
            line = line.replace(f"- {old_name}:", f"- {new_name}:")
    new_lines.append(line)

# Write the updated chat to a new file
with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"Names replaced successfully. Output saved to {output_file}")
