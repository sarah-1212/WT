import urllib.request
import re
import sys

url = "https://raw.githubusercontent.com/sarah-1212/WT/main/aeterna.pdf"

with urllib.request.urlopen(url) as response:
    data = response.read()

# Extract text between stream/endstream blocks
streams = re.findall(b'stream\r?\n(.*?)\r?\nendstream', data, re.DOTALL)

text_chunks = []
for stream in streams:
    # Decode printable ASCII text from each stream
    chunk = re.sub(b'[^\x20-\x7E\n]', b' ', stream)
    chunk = chunk.decode('ascii', errors='ignore')
    # Clean up excessive whitespace
    chunk = re.sub(r' {2,}', ' ', chunk)
    chunk = re.sub(r'\n{3,}', '\n\n', chunk)
    chunk = chunk.strip()
    if len(chunk) > 20:  # skip tiny/empty streams
        text_chunks.append(chunk)

print('\n\n'.join(text_chunks))
