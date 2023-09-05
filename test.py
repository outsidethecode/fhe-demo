import numpy as np
from concrete import fhe

def to_chunks(number, width=256, chunk_size=8):
    assert width % chunk_size == 0
    return [
        (number >> i) & ((2**chunk_size) - 1)
        for i in range(0, width, chunk_size)
    ]

def to_number(chunks, chunk_size=8):
    return sum(byte << (chunk_size * i) for i, byte in enumerate(chunks))


def add(x, y):
    return x + y

compiler = fhe.Compiler(add, {"x": "encrypted", "y": "clear"})


inputset = [
    (
        48915617476484211273115281063704461783033490425405257564258124598871191647089,
        48915617476484211273115281063704461783033490425405257564258124598871191647089,
    ),
    (
        0x0,
        0x0,
    ),
    (
        0x3350,
        0x3350,
    )
]
chunked_inputset = [tuple(to_chunks(value) for value in input) for input in inputset]

circuit = compiler.compile(chunked_inputset, show_graph=True)
circuit.keys.generate()


sample = (0x123, 0x456)
chunked_sample = tuple(to_chunks(value) for value in sample)

chunked_result = circuit.encrypt_run_decrypt(*chunked_sample)
result = to_number(chunked_result)

assert result == sample[0] + sample[1]