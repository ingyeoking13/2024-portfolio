from time import time

class Id:
    """
    data: 0-0000....0000-0-000...000-000...000 
    len: {1}-{41}-{1}-{9}-{18}
    name: sign-seconds-datacenter-server-sequence
    같은 초에 총 2^18 ~ 25만개를 생성할 수 있음 
    """

    def __init__(self, sign, timestamp, data_center, server_id, seq) -> None:
        self.sign = sign
        self.timestamp = timestamp
        self.data_center = data_center
        self.server_id = server_id
        self.seq = seq

    def __repr__(self):
        return f'{self.sign}-{self.timestamp}-{self.data_center}' +\
                f'{self.server_id}-{self.seq}'

class IdGenerator:
    """
    twitter snowflake id generator for distributed application
    """
    
    def __init__(self, data_center, server_id):
        self.sequence = 0
        self.data_center: int = data_center
        self.server_id: int = server_id
    
    def gen_id(self) -> Id:
        sign_part = '0'
        time_part = str(bin(int(time())))[2:].zfill(41)
        data_center_part = str(bin(self.data_center))[2:].zfill(1)
        server_id_part = str(bin(self.server_id))[2:].zfill(9)
        sequence_part = str(bin(self.sequence))[2:].zfill(18)
        self.sequence += 1
        return Id(sign_part, time_part, data_center_part, 
                  server_id_part, sequence_part)