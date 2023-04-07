import rhino3dm

def create_rectangular_plan(length, width, height):
    points = [
        rhino3dm.Point3d(0, 0, height),
        rhino3dm.Point3d(length, 0, height),
        rhino3dm.Point3d(length, width, height),
        rhino3dm.Point3d(0, width, height),
        rhino3dm.Point3d(0, 0, height)
    ]
    polyline = rhino3dm.Polyline(points)
    return polyline

model = rhino3dm.File3dm()

house_length = 40
house_width = 30
house_wall_height = 12
loft_height = 6
wall_thickness = 2

# Create exterior walls
exterior_walls = create_rectangular_plan(house_length, house_width, 0)
exterior_wall_extrusion = rhino3dm.Extrusion.Create(exterior_walls.ToPolylineCurve(), house_wall_height, True)
model.Objects.AddExtrusion(exterior_wall_extrusion)

# Create interior walls
interior_walls = create_rectangular_plan(house_length - wall_thickness, house_width - wall_thickness, 0)
interior_wall_extrusion = rhino3dm.Extrusion.Create(interior_walls.ToPolylineCurve(), house_wall_height, True)
model.Objects.AddExtrusion(interior_wall_extrusion)

# Create loft
loft = create_rectangular_plan(house_length, house_width * 0.5, house_wall_height - loft_height)
model.Objects.AddCurve(loft.ToPolylineCurve())

# Create roof
roof_points = [
    rhino3dm.Point3d(house_length * 0.5, 0, house_wall_height + loft_height),
    rhino3dm.Point3d(house_length * 0.5, house_width, house_wall_height + loft_height)
]
roof_line = rhino3dm.LineCurve(roof_points[0], roof_points[1])
model.Objects.AddLine(roof_points[0], roof_points[1])

model.Write("rammed_earth_house.3dm", 5)

