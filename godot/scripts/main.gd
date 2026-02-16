extends Node3D

const TRACK_LENGTH := 400.0
const STRAIGHT_LENGTH := 100.0
const HALF_STRAIGHT := STRAIGHT_LENGTH / 2.0
const CURVE_RADIUS_CENTER := 100.0 / PI
const LANE_WIDTH := 4.0
const LAPS := 4

var skaters: Array = []
var finished := false


func _ready() -> void:
	_setup_scene()
	_setup_track_visuals()
	_setup_skaters()


func _process(delta: float) -> void:
	if finished:
		return

	var done := 0
	for skater in skaters:
		skater.progress += skater.speed_mps * delta

		if skater.progress >= TRACK_LENGTH * LAPS:
			skater.progress = TRACK_LENGTH * LAPS
			done += 1

		var lane_id: int = _lane_for_progress(skater.start_lane, skater.progress)
		var p: Vector3 = _point_on_track(fmod(skater.progress, TRACK_LENGTH), lane_id)
		skater.node.global_position = p

	if done == skaters.size():
		finished = true


func _setup_scene() -> void:
	var camera := Camera3D.new()
	camera.position = Vector3(0.0, 70.0, 110.0)
	camera.rotation_degrees = Vector3(-28.0, 0.0, 0.0)
	add_child(camera)

	var light := DirectionalLight3D.new()
	light.rotation_degrees = Vector3(-45.0, 20.0, 0.0)
	add_child(light)

	var world := WorldEnvironment.new()
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.05, 0.09, 0.15)
	world.environment = env
	add_child(world)


func _setup_track_visuals() -> void:
	var ice := MeshInstance3D.new()
	var ice_mesh := PlaneMesh.new()
	ice_mesh.size = Vector2(240, 240)
	ice.mesh = ice_mesh
	ice.rotation_degrees = Vector3(-90, 0, 0)
	var ice_mat := StandardMaterial3D.new()
	ice_mat.albedo_color = Color(0.70, 0.88, 0.98)
	ice.material_override = ice_mat
	add_child(ice)

	# Finish line (typical at end of one straight)
	var finish_line := MeshInstance3D.new()
	var finish_box := BoxMesh.new()
	finish_box.size = Vector3(0.3, 0.02, LANE_WIDTH * 2.2)
	finish_line.mesh = finish_box
	finish_line.position = Vector3(HALF_STRAIGHT, 0.05, CURVE_RADIUS_CENTER)
	var finish_mat := StandardMaterial3D.new()
	finish_mat.albedo_color = Color(1, 1, 1)
	finish_line.material_override = finish_mat
	add_child(finish_line)

	# Crossover line on opposite straight (once per lap)
	var cross_line := MeshInstance3D.new()
	var cross_box := BoxMesh.new()
	cross_box.size = Vector3(0.3, 0.02, LANE_WIDTH * 2.2)
	cross_line.mesh = cross_box
	cross_line.position = Vector3(-HALF_STRAIGHT, 0.05, -CURVE_RADIUS_CENTER)
	var cross_mat := StandardMaterial3D.new()
	cross_mat.albedo_color = Color(1.0, 0.45, 0.2)
	cross_line.material_override = cross_mat
	add_child(cross_line)


func _setup_skaters() -> void:
	skaters = [
		{
			"name": "Skater A",
			"speed_mps": 11.2,
			"progress": 0.0,
			"start_lane": 0,
			"node": _make_skater_node(Color(0.95, 0.42, 0.18)),
		},
		{
			"name": "Skater B",
			"speed_mps": 11.1,
			"progress": 0.0,
			"start_lane": 1,
			"node": _make_skater_node(Color(0.19, 0.51, 0.96)),
		},
	]


func _make_skater_node(color: Color) -> MeshInstance3D:
	var body := MeshInstance3D.new()
	var m := CapsuleMesh.new()
	m.radius = 0.8
	m.height = 2.0
	body.mesh = m
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	body.material_override = mat
	add_child(body)
	return body


func _lane_for_progress(start_lane: int, progress: float) -> int:
	# Exactly one lane switch per 400m lap.
	var lap_index := int(floor(progress / TRACK_LENGTH))
	if lap_index % 2 == 0:
		return start_lane
	return 1 - start_lane


func _point_on_track(s: float, lane_id: int) -> Vector3:
	var lane_sign: float = -1.0 if lane_id == 0 else 1.0
	var radius: float = CURVE_RADIUS_CENTER + lane_sign * (LANE_WIDTH * 0.5)

	if s < 100.0:
		var t1: float = s / 100.0
		return Vector3(lerpf(-HALF_STRAIGHT, HALF_STRAIGHT, t1), 1.0, radius)
	elif s < 200.0:
		var t2: float = (s - 100.0) / 100.0
		var ang2: float = lerpf(PI * 0.5, -PI * 0.5, t2)
		return Vector3(HALF_STRAIGHT + cos(ang2) * radius, 1.0, sin(ang2) * radius)
	elif s < 300.0:
		var t3: float = (s - 200.0) / 100.0
		return Vector3(lerpf(HALF_STRAIGHT, -HALF_STRAIGHT, t3), 1.0, -radius)
	else:
		var t4: float = (s - 300.0) / 100.0
		var ang4: float = lerpf(-PI * 0.5, PI * 0.5, t4)
		return Vector3(-HALF_STRAIGHT + cos(ang4) * radius, 1.0, sin(ang4) * radius)
