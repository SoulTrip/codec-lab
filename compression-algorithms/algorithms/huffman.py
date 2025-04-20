from collections import Counter
from typing import Dict, Optional, Tuple, Union
import heapq
from bitarray import bitarray

class Node:
    def __init__(self, freq: int, byte: Optional[int] = None, left=None, right=None):
        self.freq = freq
        self.byte = byte
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:
    def __init__(self):
        self.codes: Dict[int, str] = {}
        self.reverse_codes: Dict[str, int] = {}

    def compress(self, data: Union[str, bytes], binary: bool = False) -> Tuple[bytes, Dict[int, str]]:
        if not binary:
            data = data.encode("utf-8")  # convert str to bytes

        freq = Counter(data)
        root = self._build_tree(freq)
        self._generate_codes(root)

        bit_seq = bitarray()
        for byte in data:
            bit_seq.extend(self.codes[byte])  # codes[byte] is string like "101"

        return bit_seq.tobytes(), self.codes

    def decompress(self, payload: bytes, codes: Dict[int, str], binary: bool = False) -> Union[str, bytes]:
        self.reverse_codes = {v: k for k, v in codes.items()}

        ba = bitarray()
        ba.frombytes(payload)

        curr = ""
        output = bytearray()

        for bit in ba.to01():  # returns bitstring like "0101"
            curr += bit
            if curr in self.reverse_codes:
                output.append(self.reverse_codes[curr])
                curr = ""

        return output if binary else output.decode("utf-8")

    def _build_tree(self, freq_map: Dict[int, int]) -> Node:
        heap = [Node(freq, byte=b) for b, freq in freq_map.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            n1 = heapq.heappop(heap)
            n2 = heapq.heappop(heap)
            merged = Node(n1.freq + n2.freq, left=n1, right=n2)
            heapq.heappush(heap, merged)

        return heap[0]

    def _generate_codes(self, node: Optional[Node], prefix: str = ""):
        if node is None:
            return
        if node.byte is not None:
            self.codes[node.byte] = prefix
            return
        self._generate_codes(node.left, prefix + "0")
        self._generate_codes(node.right, prefix + "1")