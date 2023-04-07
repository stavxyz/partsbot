import rhino3dm

def create_wall(start_point, end_point, wall_thickness, wall_height):
    points = [
        start_point,
        end_point,
        rhino3dm.Point3d(end_point.X, end_point.Y - wall_thickness, 0),
        rhino3dm.Point3d(start_point.X, start_point.Y - wall_thickness, 0),
        start_point
    ]
    polyline = rhino3dm.Polyline(points)
    return rhino3dm.Extrusion.Create(polyline.ToPolylineCurve(), wall_height, True)

model = rhino3dm.File3dm()

house_length = 40
house_width = 30
house_wall_height = 12
loft_height = 6
wall_thickness = 2

# Add a layer
layer = rhino3dm.Layer()
layer.Name = "House"
layer_index = model.Layers.Add(layer)

# Create walls
wall_1 = create_wall(rhino3dm.Point3d(0, house_width, 0), rhino3dm.Point3d(house_length, house_width, 0), wall_thickness, house_wall_height)
wall_2 = create_wall(rhino3dm.Point3d(house_length, house_width, 0), rhino3dm.Point3d(house_length, 0, 0), wall_thickness, house_wall_height)
wall_3 = create_wall(rhino3dm.Point3d(house_length, 0, 0), rhino3dm.Point3d(0, 0, 0), wall_thickness, house_wall_height)
wall_4 = create_wall(rhino3dm.Point3d(0, 0, 0), rhino3dm.Point3d(0, house_width, 0), wall_thickness, house_wall_height)

# Create attributes and set the layer index
attributes = rhino3dm.ObjectAttributes()
attributes.LayerIndex = layer_index

model.Objects.AddExtrusion(wall_1, attributes)
model.Objects.AddExtrusion(wall_2, attributes)
model.Objects.AddExtrusion(wall_3, attributes)
model.Objects.AddExtrusion(wall_4, attributes)

# Create loft
loft_points = [
    rhino3dm.Point3d(0, house_width * 0.5, house_wall_height - loft_height),
    rhino3dm.Point3d(house_length, house_width * 0.5, house_wall_height - loft_height)
]
loft_line = rhino3dm.LineCurve(loft_points[0], loft_points[1])
model.Objects.Add(loft_line, attributes)

# Create roof
roof_points = [
    rhino3dm.Point3d(house_length * 0.5, 0, house_wall_height + loft_height),
    rhino3dm.Point3d(house_length * 0.5, house_width, house_wall_height + loft_height)
]
roof_line = rhino3dm.LineCurve(roof_points[0], roof_points[1])
model.Objects.Add(roof_line, attributes)

model.Write("rammed_earth_house.3dm", 5)

