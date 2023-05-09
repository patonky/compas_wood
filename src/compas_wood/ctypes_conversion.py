from ctypes import *
from compas.geometry import Polyline
from compas.geometry import Point


# # Convert the nested list to a flat list
# flat_list = [item for sublist in nested_list for item in sublist]

# # Convert the flat list to a ctypes array
# c_array = (ctypes.c_int * len(flat_list))(*flat_list)


def list_polylines_coord(polylines):
    f = []
    v = []
    for polyline in polylines:
        f.append(len(polyline))
        for point in polyline:
            v.extend(point)
    _f = (c_size_t * len(f))(*f)
    _v = (c_float * len(v))(*v)
    return _f, c_size_t(len(f)), _v, c_size_t(len(v))


def lists_vectors_coord(vectors):
    faces = [len(v) for v in vectors]
    f = (c_size_t * len(vectors))(*faces)
    v = [coord for vec in vectors for point in vec for coord in point]

    v_s = c_size_t(len(v))  # * sizeof(c_float)
    v = (c_float * len(v))(*v)
    return f, c_size_t(len(vectors)), v, v_s


def lists_numbers_coord(numbers):
    v_s = 0
    f_s = len(numbers)
    f = (c_size_t * len(numbers))()

    for i in range(len(numbers)):
        f[i] = len(numbers[i])
        v_s += len(numbers[i]) * 1

    v = (c_int * v_s)()

    count = 0
    for i in range(len(numbers)):
        for j in range(len(numbers[i])):
            v[count] = numbers[i][j]
            count += 1

    return f, c_size_t(f_s), v, c_size_t(v_s)


def list_ints_coord(numbers):
    f_s = len(numbers)
    f = [0.0] * f_s
    for i in range(f_s):
        f[i] = numbers[i]
    return (c_int * len(f))(*f), c_size_t(f_s)


def list_numbers_coord(numbers):
    f_s = len(numbers)
    f = [0.0] * f_s
    for i in range(f_s):
        f[i] = numbers[i]
    return (c_float * len(f))(*f), c_size_t(f_s)


# import concurrent.futures


# def create_polyline(points, polyline):
#     polyline.points = [Point(*point) for point in points]
#     return polyline


# def coord_polylines_lists_threaded(
#     groups_f, groups_f_s, out_f, out_f_s, out_v, out_v_s
# ):
#     polylines = [
#         [Polyline([]) for j in range(groups_f[i])] for i in range(groups_f_s.value)
#     ]

#     a = 0
#     b = 0
#     pline_count = 0
#     num_points = 3
#     num_groups = groups_f_s.value

#     points = []
#     futures = []
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         for i in range(0, out_v_s.value, num_points):
#             points.append([out_v[i], out_v[i + 1], out_v[i + 2]])
#             num_points_per_polyline = out_f[pline_count]

#             if len(points) == num_points_per_polyline:
#                 polyline = polylines[a][b]
#                 futures.append(executor.submit(create_polyline, points, polyline))
#                 points = []
#                 num_polylines_per_group = groups_f[a]
#                 if b == (num_polylines_per_group - 1):
#                     a += 1
#                     b = 0
#                 else:
#                     b += 1
#                 pline_count += 1

#     for future in concurrent.futures.as_completed(futures):
#         future.result()

#     return polylines


def coord_polylines_lists(groups_f, groups_f_s, out_f, out_f_s, out_v, out_v_s):
    polylines = [
        [Polyline([]) for j in range(groups_f[i])] for i in range(groups_f_s.value)
    ]

    a = 0
    b = 0
    pline_count = 0
    num_points = 3
    num_groups = groups_f_s.value

    points = []
    for i in range(0, out_v_s.value, num_points):
        points.append([out_v[i], out_v[i + 1], out_v[i + 2]])
        num_points_per_polyline = out_f[pline_count]

        if len(points) == num_points_per_polyline:
            for j in range(a, groups_f_s.value):
                if groups_f[j] > 0:
                    a = j
                    break

            polylines[a][b] = Polyline(points)
            points = []
            num_polylines_per_group = groups_f[a]
            if b == (num_polylines_per_group - 1):
                a += 1
                b = 0
            else:
                b += 1
            pline_count += 1

    return polylines


# def coord_polylines_lists(groups_f, groups_f_s, out_f, out_f_s, out_v, out_v_s):
#     # create Python polylines
#     polylines = [
#         [Polyline([]) for j in range(groups_f[i])] for i in range(groups_f_s.value)
#     ]

#     """
#     polylines = [[None] * groups_f[i] for i in range(groups_f_s.value)]

#     face_count = 0
#     for i in range(groups_f_s.value):
#         for j in range(groups_f[i]):
#             polylines[i][j] = Polyline([])  # Polyline(out_f[face_count])
#             face_count += 1
#     """
#     # fill polylines with points
#     # a = 0
#     # b = 0
#     # pline_count = 0

#     # for i in range(0, out_v_s.value, 3):
#     #     polylines[a][b].points.append(Point(out_v[i], out_v[i + 1], out_v[i + 2]))

#     #     if len(polylines[a][b]) == out_f[pline_count]:
#     #         if b == (groups_f[a] - 1):
#     #             a += 1
#     #             b = 0
#     #         else:
#     #             b += 1
#     #         pline_count += 1
#     a = 0
#     b = 0
#     pline_count = 0
#     num_points = 3
#     num_groups = groups_f_s.value

#     for i in range(0, out_v_s.value, num_points):
#         polyline = polylines[a][b]
#         polyline.points.append(Point(out_v[i], out_v[i + 1], out_v[i + 2]))

#         num_points_per_polyline = out_f[pline_count]
#         if len(polyline) == num_points_per_polyline:
#             num_polylines_per_group = groups_f[a]
#             if b == (num_polylines_per_group - 1):
#                 a += 1
#                 b = 0
#             else:
#                 b += 1
#             pline_count += 1
#     # output
#     return polylines


def coord_numbers_lists(out_f, out_f_s, out_v, out_v_s):
    # transfer data from C++
    # sharp_out_f = (c_int * out_f_s)()
    # sharp_out_v = (c_int * out_v_s)()
    # ctypes.memmove(sharp_out_f, out_f, out_f_s * sizeof(c_int))
    # ctypes.memmove(sharp_out_v, out_v, out_v_s * sizeof(c_int))
    # ctypes.windll.kernel32.GlobalFree(out_f)
    # ctypes.windll.kernel32.GlobalFree(out_v)

    # create Python objects
    ids = [[] for _ in range(out_f_s.value)]

    for i in range(out_f_s.value):
        ids[i] = [None] * out_f[i]
        if out_f[i] == 0:
            return

    # fill array with points
    a = 0
    b = 0
    for i in range(0, out_v_s.value):
        ids[a][b] = out_v[i]
        if b == (out_f[a] - 1):
            a += 1
            b = 0
        else:
            b += 1

    return ids