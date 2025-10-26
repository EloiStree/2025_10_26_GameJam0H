extends Node

#List of ipv4:port to target
@export var list_targets_ipv4: Array[String] = ["127.0.0.1:4615"]

var udp_socket := PacketPeerUDP.new()

func push_text_to_targets(text_to_send_utf8: String):
	var bytes_to_send = text_to_send_utf8.to_utf8_buffer()
	push_bytes_to_targets(bytes_to_send)

func push_bytes_to_targets(bytes_to_send: PackedByteArray):
	for target in list_targets_ipv4:
		var parts = target.split(":")
		if parts.size() == 2:
			var ip = parts[0]
			var port = parts[1].to_int()
			udp_socket.connect_to_host(ip, port)
			udp_socket.put_packet(bytes_to_send)
			udp_socket.close()

func var_to_int32_bytes(value_int32: int) -> PackedByteArray:
	var byte_array = PackedByteArray()
	byte_array.resize(4)
	byte_array[0] = value_int32 & 0xFF
	byte_array[1] = (value_int32 >> 8) & 0xFF
	byte_array[2] = (value_int32 >> 16) & 0xFF
	byte_array[3] = (value_int32 >> 24) & 0xFF
	return byte_array

func var_to_ulong64bytes(value_ulong64: int) -> PackedByteArray:
	var byte_array = PackedByteArray()
	byte_array.resize(8)
	byte_array[0] = value_ulong64 & 0xFF
	byte_array[1] = (value_ulong64 >> 8) & 0xFF
	byte_array[2] = (value_ulong64 >> 16) & 0xFF
	byte_array[3] = (value_ulong64 >> 24) & 0xFF
	byte_array[4] = (value_ulong64 >> 32) & 0xFF
	byte_array[5] = (value_ulong64 >> 40) & 0xFF
	byte_array[6] = (value_ulong64 >> 48) & 0xFF
	byte_array[7] = (value_ulong64 >> 56) & 0xFF
	return byte_array


func push_iid_to_targets(index_int32: int, value_int32: int, date_ulong64: int):

	var byte_as_int_index = var_to_int32_bytes(index_int32)
	var byte_as_int_value = var_to_int32_bytes(value_int32)
	var byte_as_ulong_date = var_to_ulong64bytes(date_ulong64)

	var bytes_as_iid = PackedByteArray()
	bytes_as_iid.append_array(byte_as_int_index)
	bytes_as_iid.append_array(byte_as_int_value)
	bytes_as_iid.append_array(byte_as_ulong_date)
	push_bytes_to_targets(bytes_as_iid)
