extends Node

@export var allowed_ipv4_array=["127.0.0.1"]
@export var allowed_port=3615

var udp_server: UDPServer

signal on_iid_data_received(index_int32: int, value_int32: int, date_ulong64: int)

func _ready() -> void:
	udp_server = UDPServer.new()
	var result = udp_server.listen(allowed_port)
	if result != OK:
		print("Failed to start UDP server on port ", allowed_port)
	else:
		print("UDP server listening on port ", allowed_port)

func _process(_delta) -> void:
	udp_server.poll()
	
	if udp_server.is_connection_available():
		var peer = udp_server.take_connection()
		var ip = peer.get_packet_ip()
		
		if ip in allowed_ipv4_array:
			var packet = peer.get_packet()
			if packet.size() > 0:
				_handle_received_data(packet, ip)
		else:
			print("Rejected connection from unauthorized IP: ", ip)

func _handle_received_data(data: PackedByteArray, from_ip: String) -> void:
	if data.size() >= 16:  # 4 + 4 + 8 bytes for int, int, uint64
		var index = data.decode_s32(0)
		var value = data.decode_s32(4)
		var date = data.decode_u64(8)
		print("Received - Index: ", index, ", Value: ", value, ", Date: ", date)
		emit_signal("on_iid_data_received", index, value, date)
	else:
		print("Invalid packet size from ", from_ip)
