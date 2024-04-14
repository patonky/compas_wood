import wood_nano
from wood_nano.conversions_python import to_int2, to_int1, to_double1, from_cut_type2
from numpy import double
from compas_wood.conversions_compas import to_point2, to_vector2, from_point3




def get_connection_zones(
    input_polyline_pairs,
    input_insertion_vectors=[],
    input_joint_types=[],
    input_three_valence_element_indices_and_instruction=[],
    input_adjacency=[],
    input_joint_parameters_and_types=[],
    input_search_type=0,
    input_scale=[1, 1, 1],
    input_output_type=3,
    input_joint_volume_parameters=[0, 0, 0],
    face_to_face_side_to_side_joints_all_treated_as_rotated=False,
    input_custom_joints=[],
    input_custom_joints_types=[],

):  
    
    w_output_plines = wood_nano.point3()
    w_output_types = wood_nano.cut_type2()

    wood_nano.get_connection_zones(
        to_point2(input_polyline_pairs),
        to_vector2(input_insertion_vectors),
        to_int2(input_joint_types),
        to_int2(input_three_valence_element_indices_and_instruction),
        to_int1(input_adjacency),
        to_double1(input_joint_parameters_and_types),
        int(input_search_type),
        to_double1(input_scale),
        int(input_output_type),
        w_output_plines,
        w_output_types,
        to_double1(input_joint_volume_parameters),
        bool(face_to_face_side_to_side_joints_all_treated_as_rotated),
        to_point2(input_custom_joints),
        to_int1(input_custom_joints_types),
    )


    return from_point3(w_output_plines), from_cut_type2(w_output_types)



if __name__ == "__main__":

    from compas.geometry import Point, Polyline
    from  compas_wood import data_sets_plates

  # joinery parameters
    division_length = 300
    joint_parameters = [
        division_length,
        0.5,
        9,
        division_length * 1.5,
        0.65,
        10,
        division_length * 1.5,
        0.5,
        21,
        division_length,
        0.95,
        30,
        division_length,
        0.95,
        40,
        division_length,
        0.95,
        50,
    ]

    # generate joints
    output_polylines, output_types = get_connection_zones(
        data_sets_plates.annen_small_polylines(),
        data_sets_plates.annen_small_edge_directions(),
        data_sets_plates.annen_small_edge_joints(),
        data_sets_plates.annen_small_three_valance_element_indices_and_instruction(),
        [],
        joint_parameters,
        0,
        [1, 1, 1],
        4   
    )

    import sys
    if sys.version_info >= (3, 9):

        from compas_viewer import Viewer
        from compas.geometry import Scale
        scale = 1e-3
        scale_transform = Scale.from_factors([scale, scale, scale])
        viewer = Viewer()
        for polylines in output_polylines:
            for polyline in polylines:
                polyline.transform(scale_transform)
                viewer.scene.add(Polyline(polyline), show_points=False)
        
        viewer.show()
