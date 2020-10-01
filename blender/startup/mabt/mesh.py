"""
Quaternion experimentation
"""
import time
import collections

import bpy
import bmesh
import mathutils


def get_islands(mesh_data):
    """"""
    bm = bmesh.new()
    bm.from_mesh(mesh_data)

    island_idx = 0
    islands = collections.defaultdict(set)
    tag = [False] * len(bm.verts)

    for v in bm.verts:

        if tag[v.index]:
            continue

        verts = set([v])
        while verts:

            current_vert = verts.pop()
            if tag[current_vert.index]:
                continue

            tag[current_vert.index] = True

            for edge in current_vert.link_edges:
                for vert in edge.verts:
                    if tag[vert.index]:
                        continue

                    verts.add(vert)
                    islands[island_idx].add(vert)

        island_idx += 1
    return islands
