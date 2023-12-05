from .Constant import *
from .Hamming import *
import hashlib

def breakdown_file(data: bytes) -> list:
    list_data = []
    hamming = Hamming()
    half_payload = PAYLOAD_SIZE // 2
    total_chunks = len(data) // half_payload
    if total_chunks == 0: total_chunks = 1
    processed_chunks = 0

    def update_progress_bar():
        nonlocal processed_chunks
        progress = processed_chunks / total_chunks
        bar_length = 40
        bar = '=' * int(bar_length * progress) + '-' * (bar_length - int(bar_length * progress))
        print(f"\rConverting to bytes: [{bar}] {int(progress * 100)}%", end='', flush=True)

    while len(data) > 0:
        if len(data) > half_payload:
            encoded_data = hamming.breakdownDataToBytes(data[:half_payload])
            list_data.append(encoded_data)
            data = data[half_payload:]
        else:
            encoded_data = hamming.breakdownDataToBytes(data)
            list_data.append(encoded_data)
            data = b''
        processed_chunks += 1
        update_progress_bar()

    print()  # Print a new line after the progress bar is complete
    return list_data

def merge_file(list_data: list) -> bytes:
    data = b''
    for i in list_data:
        data += i
    return data

def encode_metadata(data: bytes) -> bytes:
    hamming = Hamming()
    encodedData = hamming.breakdownDataToBytes(data)
    return encodedData

def decode_metadata(data: bytes) -> bytes:
    hamming = Hamming()
    decodedData = hamming.breakdownBytes(data)
    return decodedData

def printmd5(data: str):
    with open(data, 'rb') as file_obj:
        file_contents = file_obj.read()
        md5_hash = hashlib.md5(file_contents).hexdigest()
        return md5_hash