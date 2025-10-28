import struct


class BulletCreationPoint:
    # Represents the instantiation of a bullet in the server game
    def __init__(self):
        self.ulong_server_timestamp = 0  # ulong
        self.byte_pool_id = 0  # byte
        self.int_bullet_id = 0  # int
        self.int_owner_id = 0  # int
        self.float3_start_position = [0.0, 0.0, 0.0]  # float 3
        self.float3_start_direction = [0.0, 0.0, 0.0]  # float 3
        self.float_diameter = 0.0  # float
        self.uint_speed_per_second_mm = 0  # uint

    def get_bullet_position_at_given_relative_time(self, relative_time_ms: int) -> list[float]:
        # Calculate the position of the bullet at a given time (in milliseconds) since instantiation
        time_seconds = relative_time_ms / 1000.0
        position = [
            self.start_position[0] + self.start_direction[0] * self.speed_per_second_mm * time_seconds / 1000.0,
            self.start_position[1] + self.start_direction[1] * self.speed_per_second_mm * time_seconds / 1000.0,
            self.start_position[2] + self.start_direction[2] * self.speed_per_second_mm * time_seconds / 1000.0,
        ]
        return position
    
    def get_bullet_position_at_absolute_time(self, absolute_time_ms: int) -> list[float]:
        # Calculate the position of the bullet at a given absolute time (in milliseconds)
        relative_time_ms = absolute_time_ms - self.ulong_server_timestamp
        return self.get_bullet_position_at_given_relative_time(relative_time_ms)
  
    def to_bytes(self) -> bytes:
        # Pack: ulong(Q) + byte(B) + int(i) + int(i) + 3*float(f) + 3*float(f) + float(f) + uint(I)
        return struct.pack('<QBii3f3ffI', 
                  self.ulong_server_timestamp,
                  self.byte_pool_id,
                  self.int_bullet_id,
                  self.int_owner_id,
                  self.float3_start_position[0], self.float3_start_position[1], self.float3_start_position[2],
                  self.float3_start_direction[0], self.float3_start_direction[1], self.float3_start_direction[2],
                  self.float_diameter,
                  self.uint_speed_per_second_mm)

    def get_bytes_size() -> int:
        return struct.calcsize('<QBii3f3ffI')

    @classmethod
    def from_bytes(cls, data: bytes):
        unpacked = struct.unpack('<QBii3f3ffI', data)
        instance = cls()
        instance.ulong_server_timestamp = unpacked[0]
        instance.byte_pool_id = unpacked[1]
        instance.int_bullet_id = unpacked[2]
        instance.int_owner_id = unpacked[3]
        instance.float3_start_position = [unpacked[4], unpacked[5], unpacked[6]]
        instance.float3_start_direction = [unpacked[7], unpacked[8], unpacked[9]]
        instance.float_diameter = unpacked[10]
        instance.uint_speed_per_second_mm = unpacked[11]
        return instance


class BulletDestructionPoint:
    # Represents the destruction of a bullet in the server game
    def __init__(self):
        self.ulong_server_timestamp = 0  # ulong
        self.byte_pool_id = 0  # byte
        self.int_bullet_id = 0  # int
        self.float3_end_position = [0.0, 0.0, 0.0]  # float 3

    def get_bytes_size() -> int:
        return struct.calcsize('<QBi3f')

    def to_bytes(self) -> bytes:
        # Pack: ulong(Q) + byte(B) + int(i) + 3*float(f)
        return struct.pack('<QBi3f', 
                          self.ulong_server_timestamp,
                          self.byte_pool_id,
                          self.int_bullet_id,
                          self.float3_end_position[0], self.float3_end_position[1], self.float3_end_position[2])
    
    @classmethod
    def from_bytes(cls, data: bytes):
        unpacked = struct.unpack('<QBi3f', data)
        instance = cls()
        instance.ulong_server_timestamp = unpacked[0]
        instance.byte_pool_id = unpacked[1]
        instance.int_bullet_id = unpacked[2]
        instance.float3_end_position = [unpacked[3], unpacked[4], unpacked[5]]
        return instance



class BulletHellGame:

    def is_player_bytes_information(byte_array:bytes) -> bool:
        return byte_array.startswith(b'\x01\x02\x03') and byte_array.endswith(b'\x03\x02\x01')

    def is_bullet_bytes_information(byte_array:bytes) -> bool:        
        return byte_array.startswith(b'\x03\x02\x01') and byte_array.endswith(b'\x01\x02\x03')
    
    def is_bullet_bytes_instanciation_information(byte_array:bytes) -> bool:
        expected_size = BulletCreationPoint.get_bytes_size() + 6  # 6 bytes for start and end markers
        return (len(byte_array) == expected_size and
                byte_array.startswith(b'\x03\x02\x01') and 
                byte_array.endswith(b'\x01\x02\x03'))
    def is_bullet_bytes_destruction_information(byte_array:bytes) -> bool:
        expected_size = BulletDestructionPoint.get_bytes_size() + 6  # 6 bytes for start and end markers
        return (len(byte_array) == expected_size and
                byte_array.startswith(b'\x03\x02\x01') and 
                byte_array.endswith(b'\x01\x02\x03'))
    
    def parse_bytes_to_bullet_start_point(byte_array:bytes) -> BulletCreationPoint:
        if not BulletHellGame.is_bullet_bytes_instanciation_information(byte_array):
            raise ValueError("Invalid bullet instantiation byte array")
        # Remove start and end markers
        core_data = byte_array[3:-3]
        return BulletCreationPoint.from_bytes(core_data)

    def parse_bytes_to_bullet_destruction_point(byte_array:bytes) -> BulletDestructionPoint:
        if not BulletHellGame.is_bullet_bytes_destruction_information(byte_array):
            raise ValueError("Invalid bullet destruction byte array")
        # Remove start and end markers
        core_data = byte_array[3:-3]
        return BulletDestructionPoint.from_bytes(core_data)



