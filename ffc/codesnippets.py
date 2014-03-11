"Code snippets for code generation."

# Copyright (C) 2007-2013 Anders Logg
#
# This file is part of FFC.
#
# FFC is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FFC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with FFC. If not, see <http://www.gnu.org/licenses/>.
#
# Modified by Kristian B. Oelgaard 2010-2013
# Modified by Marie Rognes 2007-2012
# Modified by Peter Brune 2009
# Modified by Martin Alnaes, 2013
#
# First added:  2007-02-28
# Last changed: 2014-03-11

# Code snippets

__all__ = ["comment_ufc", "comment_dolfin", "header_h", "header_c", "footer",
           "compute_jacobian", "compute_jacobian_inverse",
           "eval_basis_decl", "eval_basis", "eval_basis_copy",
           "eval_derivs_decl", "eval_derivs", "eval_derivs_copy"]

__old__ = ["evaluate_f",
           "facet_determinant", "map_onto_physical",
           "fiat_coordinate_map", "transform_snippet",
           "scale_factor", "combinations_snippet",
           "normal_direction",
           "facet_normal", "ip_coordinates", "cell_volume", "circumradius",
           "facet_area", "min_facet_edge_length", "max_facet_edge_length",
           "orientation_snippet"]

__all__ += __old__

comment_ufc = """\
// This code conforms with the UFC specification version %(ufc_version)s
// and was automatically generated by FFC version %(ffc_version)s.
"""

comment_dolfin = """\
// This code conforms with the UFC specification version %(ufc_version)s
// and was automatically generated by FFC version %(ffc_version)s.
//
// This code was generated with the option '-l dolfin' and
// contains DOLFIN-specific wrappers that depend on DOLFIN.
"""

# Code snippets for headers and footers

header_h = """\
#ifndef __%(prefix_upper)s_H
#define __%(prefix_upper)s_H

#include <cmath>
#include <stdexcept>
#include <fstream>
#include <ufc.h>
"""

header_c = """\
#include "%(prefix)s.h"
"""

footer = """\
#endif
"""

# Code snippets for computing Jacobians

_compute_jacobian_interval_1d = """\
// Compute Jacobian
double J%(restriction)s[1];
compute_jacobian_interval_1d(J%(restriction)s, vertex_coordinates%(restriction)s);
"""

_compute_jacobian_interval_2d = """\
// Compute Jacobian
double J%(restriction)s[2];
compute_jacobian_interval_2d(J%(restriction)s, vertex_coordinates%(restriction)s);
"""

_compute_jacobian_interval_3d = """\
// Compute Jacobian
double J%(restriction)s[3];
compute_jacobian_interval_3d(J%(restriction)s, vertex_coordinates%(restriction)s);
"""

_compute_jacobian_triangle_2d = """\
// Compute Jacobian
double J%(restriction)s[4];
compute_jacobian_triangle_2d(J%(restriction)s, vertex_coordinates%(restriction)s);
"""

_compute_jacobian_triangle_3d = """\
// Compute Jacobian
double J%(restriction)s[6];
compute_jacobian_triangle_3d(J%(restriction)s, vertex_coordinates%(restriction)s);
"""

_compute_jacobian_tetrahedron_3d = """\
// Compute Jacobian
double J%(restriction)s[9];
compute_jacobian_tetrahedron_3d(J%(restriction)s, vertex_coordinates%(restriction)s);
"""

compute_jacobian = {1: {1: _compute_jacobian_interval_1d,
                        2: _compute_jacobian_interval_2d,
                        3: _compute_jacobian_interval_3d},
                    2: {2: _compute_jacobian_triangle_2d,
                        3: _compute_jacobian_triangle_3d},
                    3: {3: _compute_jacobian_tetrahedron_3d}}

# Code snippets for computing Jacobian inverses

_compute_jacobian_inverse_interval_1d = """\
// Compute Jacobian inverse and determinant
double K%(restriction)s[1];
double detJ%(restriction)s;
compute_jacobian_inverse_interval_1d(K%(restriction)s, detJ%(restriction)s, J%(restriction)s);
"""

_compute_jacobian_inverse_interval_2d = """\
// Compute Jacobian inverse and determinant
double K%(restriction)s[2];
double detJ%(restriction)s;
compute_jacobian_inverse_interval_2d(K%(restriction)s, detJ%(restriction)s, J%(restriction)s);
"""

_compute_jacobian_inverse_interval_3d = """\
// Compute Jacobian inverse and determinant
double K%(restriction)s[3];
double detJ%(restriction)s;
compute_jacobian_inverse_interval_3d(K%(restriction)s, detJ%(restriction)s, J%(restriction)s);
"""

_compute_jacobian_inverse_triangle_2d = """\
// Compute Jacobian inverse and determinant
double K%(restriction)s[4];
double detJ%(restriction)s;
compute_jacobian_inverse_triangle_2d(K%(restriction)s, detJ%(restriction)s, J%(restriction)s);
"""

_compute_jacobian_inverse_triangle_3d = """\
// Compute Jacobian inverse and determinant
double K%(restriction)s[6];
double detJ%(restriction)s;
compute_jacobian_inverse_triangle_3d(K%(restriction)s, detJ%(restriction)s, J%(restriction)s);
"""

_compute_jacobian_inverse_tetrahedron_3d = """\
// Compute Jacobian inverse and determinant
double K%(restriction)s[9];
double detJ%(restriction)s;
compute_jacobian_inverse_tetrahedron_3d(K%(restriction)s, detJ%(restriction)s, J%(restriction)s);
"""

compute_jacobian_inverse = {1: {1: _compute_jacobian_inverse_interval_1d,
                                2: _compute_jacobian_inverse_interval_2d,
                                3: _compute_jacobian_inverse_interval_3d},
                            2: {2: _compute_jacobian_inverse_triangle_2d,
                                3: _compute_jacobian_inverse_triangle_3d},
                            3: {3: _compute_jacobian_inverse_tetrahedron_3d}}

# Code snippet for scale factor
scale_factor = """\
// Set scale factor
const double det = std::abs(detJ);"""

# FIXME: Old stuff below that should be cleaned up or moved to ufc_geometry.h

orientation_snippet = """
// Check orientation
if (cell_orientation == -1)
  throw std::runtime_error("cell orientation must be defined (not -1)");
// (If cell_orientation == 1 = down, multiply det(J) by -1)
else if (cell_orientation == 1)
  detJ%(restriction)s *= -1;
"""

evaluate_f = "f.evaluate(vals, y, c);"

_facet_determinant_1D = """\
// Facet determinant 1D (vertex)
const double det = 1.0;"""

_facet_determinant_2D = """\
// Get vertices on edge
static unsigned int edge_vertices[3][2] = {{1, 2}, {0, 2}, {0, 1}};
const unsigned int v0 = edge_vertices[facet%(restriction)s][0];
const unsigned int v1 = edge_vertices[facet%(restriction)s][1];

// Compute scale factor (length of edge scaled by length of reference interval)
const double dx0 = vertex_coordinates%(restriction)s[2*v1 + 0] - vertex_coordinates%(restriction)s[2*v0 + 0];
const double dx1 = vertex_coordinates%(restriction)s[2*v1 + 1] - vertex_coordinates%(restriction)s[2*v0 + 1];
const double det = std::sqrt(dx0*dx0 + dx1*dx1);
"""

_facet_determinant_2D_1D = """\
// Facet determinant 1D in 2D (vertex)
const double det = 1.0;
"""

_facet_determinant_3D = """\
// Get vertices on face
static unsigned int face_vertices[4][3] = {{1, 2, 3}, {0, 2, 3}, {0, 1, 3}, {0, 1, 2}};
const unsigned int v0 = face_vertices[facet%(restriction)s][0];
const unsigned int v1 = face_vertices[facet%(restriction)s][1];
const unsigned int v2 = face_vertices[facet%(restriction)s][2];

// Compute scale factor (area of face scaled by area of reference triangle)
const double a0 = (vertex_coordinates%(restriction)s[3*v0 + 1]*vertex_coordinates%(restriction)s[3*v1 + 2]  + vertex_coordinates%(restriction)s[3*v0 + 2]*vertex_coordinates%(restriction)s[3*v2 + 1]  + vertex_coordinates%(restriction)s[3*v1 + 1]*vertex_coordinates%(restriction)s[3*v2 + 2]) - (vertex_coordinates%(restriction)s[3*v2 + 1]*vertex_coordinates%(restriction)s[3*v1 + 2] + vertex_coordinates%(restriction)s[3*v2 + 2]*vertex_coordinates%(restriction)s[3*v0 + 1] + vertex_coordinates%(restriction)s[3*v1 + 1]*vertex_coordinates%(restriction)s[3*v0 + 2]);

const double a1 = (vertex_coordinates%(restriction)s[3*v0 + 2]*vertex_coordinates%(restriction)s[3*v1 + 0]  + vertex_coordinates%(restriction)s[3*v0 + 0]*vertex_coordinates%(restriction)s[3*v2 + 2] + vertex_coordinates%(restriction)s[3*v1 + 2]*vertex_coordinates%(restriction)s[3*v2 + 0]) - (vertex_coordinates%(restriction)s[3*v2 + 2]*vertex_coordinates%(restriction)s[3*v1 + 0]  + vertex_coordinates%(restriction)s[3*v2 + 0]*vertex_coordinates%(restriction)s[3*v0 + 2] + vertex_coordinates%(restriction)s[3*v1 + 2]*vertex_coordinates%(restriction)s[3*v0 + 0]);

const double a2 = (vertex_coordinates%(restriction)s[3*v0 + 0]*vertex_coordinates%(restriction)s[3*v1 + 1]  + vertex_coordinates%(restriction)s[3*v0 + 1]*vertex_coordinates%(restriction)s[3*v2 + 0]  + vertex_coordinates%(restriction)s[3*v1 + 0]*vertex_coordinates%(restriction)s[3*v2 + 1]) - (vertex_coordinates%(restriction)s[3*v2 + 0]*vertex_coordinates%(restriction)s[3*v1 + 1]  + vertex_coordinates%(restriction)s[3*v2 + 1]*vertex_coordinates%(restriction)s[3*v0 + 0]  + vertex_coordinates%(restriction)s[3*v1 + 0]*vertex_coordinates%(restriction)s[3*v0 + 1]);

const double det = std::sqrt(a0*a0 + a1*a1 + a2*a2);
"""

_facet_determinant_3D_2D = """\
// Facet determinant 2D in 3D (edge)
// Get vertices on edge
static unsigned int edge_vertices[3][2] = {{1, 2}, {0, 2}, {0, 1}};
const unsigned int v0 = edge_vertices[facet%(restriction)s][0];
const unsigned int v1 = edge_vertices[facet%(restriction)s][1];

// Compute scale factor (length of edge scaled by length of reference interval)
const double dx0 = vertex_coordinates%(restriction)s[3*v1 + 0] - vertex_coordinates%(restriction)s[3*v0 + 0];
const double dx1 = vertex_coordinates%(restriction)s[3*v1 + 1] - vertex_coordinates%(restriction)s[3*v0 + 1];
const double dx2 = vertex_coordinates%(restriction)s[3*v1 + 2] - vertex_coordinates%(restriction)s[3*v0 + 2];
const double det = std::sqrt(dx0*dx0 + dx1*dx1 + dx2*dx2);
"""

_facet_determinant_3D_1D = """\
// Facet determinant 1D in 3D (vertex)
const double det = 1.0;
"""

_normal_direction_1D = """\
const bool direction = facet%(restriction)s == 0 ? vertex_coordinates%(restriction)s[0] > vertex_coordinates%(restriction)s[1] : vertex_coordinates%(restriction)s[1] > vertex_coordinates%(restriction)s[0];
"""

_normal_direction_2D = """\
const bool direction = dx1*(vertex_coordinates%(restriction)s[2*%(facet)s] - vertex_coordinates%(restriction)s[2*v0]) - dx0*(vertex_coordinates%(restriction)s[2*%(facet)s + 1] - vertex_coordinates%(restriction)s[2*v0 + 1]) < 0;
"""

_normal_direction_3D = """\
const bool direction = a0*(vertex_coordinates%(restriction)s[3*%(facet)s] - vertex_coordinates%(restriction)s[3*v0]) + a1*(vertex_coordinates%(restriction)s[3*%(facet)s + 1] - vertex_coordinates%(restriction)s[3*v0 + 1])  + a2*(vertex_coordinates%(restriction)s[3*%(facet)s + 2] - vertex_coordinates%(restriction)s[3*v0 + 2]) < 0;
"""

# MER: Coding all up in _facet_normal_ND_M_D for now; these are
# therefore empty.
_normal_direction_2D_1D = ""
_normal_direction_3D_2D = ""
_normal_direction_3D_1D = ""

_facet_normal_1D = """
// Facet normals are 1.0 or -1.0:   (-1.0) <-- X------X --> (1.0)
const double n%(restriction)s = %(direction)sdirection ? 1.0 : -1.0;"""

_facet_normal_2D = """\
// Compute facet normals from the facet scale factor constants
const double n%(restriction)s0 = %(direction)sdirection ? dx1 / det : -dx1 / det;
const double n%(restriction)s1 = %(direction)sdirection ? -dx0 / det : dx0 / det;"""

_facet_normal_2D_1D = """
// Compute facet normal
double n%(restriction)s0 = 0.0;
double n%(restriction)s1 = 0.0;
if (facet%(restriction)s == 0)
{
  n%(restriction)s0 = vertex_coordinates%(restriction)s[0] - vertex_coordinates%(restriction)s[2];
  n%(restriction)s1 = vertex_coordinates%(restriction)s[1] - vertex_coordinates%(restriction)s[3];
}
else
{
  n%(restriction)s0 = vertex_coordinates%(restriction)s[2] - vertex_coordinates%(restriction)s[0];
  n%(restriction)s1 = vertex_coordinates%(restriction)s[3] - vertex_coordinates%(restriction)s[1];
}
const double n%(restriction)s_length = std::sqrt(n%(restriction)s0*n%(restriction)s0 + n%(restriction)s1*n%(restriction)s1);
n%(restriction)s0 /= n%(restriction)s_length;
n%(restriction)s1 /= n%(restriction)s_length;
"""

_facet_normal_3D = """
const double n%(restriction)s0 = %(direction)sdirection ? a0 / det : -a0 / det;
const double n%(restriction)s1 = %(direction)sdirection ? a1 / det : -a1 / det;
const double n%(restriction)s2 = %(direction)sdirection ? a2 / det : -a2 / det;"""

_facet_normal_3D_2D = """
// Compute facet normal for triangles in 3D
const unsigned int vertex%(restriction)s0 = facet%(restriction)s;

// Get coordinates corresponding the vertex opposite this
// static unsigned int edge_vertices[3][2] = {{1, 2}, {0, 2}, {0, 1}};
const unsigned int vertex%(restriction)s1 = edge_vertices[facet%(restriction)s][0];
const unsigned int vertex%(restriction)s2 = edge_vertices[facet%(restriction)s][1];

// Define vectors n = (p2 - p0) and t = normalized (p2 - p1)
double n%(restriction)s0 = vertex_coordinates%(restriction)s[3*vertex%(restriction)s2 + 0] - vertex_coordinates%(restriction)s[3*vertex%(restriction)s0 + 0];
double n%(restriction)s1 = vertex_coordinates%(restriction)s[3*vertex%(restriction)s2 + 1] - vertex_coordinates%(restriction)s[3*vertex%(restriction)s0 + 1];
double n%(restriction)s2 = vertex_coordinates%(restriction)s[3*vertex%(restriction)s2 + 2] - vertex_coordinates%(restriction)s[3*vertex%(restriction)s0 + 2];

double t%(restriction)s0 = vertex_coordinates%(restriction)s[3*vertex%(restriction)s2 + 0] - vertex_coordinates%(restriction)s[3*vertex%(restriction)s1 + 0];
double t%(restriction)s1 = vertex_coordinates%(restriction)s[3*vertex%(restriction)s2 + 1] - vertex_coordinates%(restriction)s[3*vertex%(restriction)s1 + 1];
double t%(restriction)s2 = vertex_coordinates%(restriction)s[3*vertex%(restriction)s2 + 2] - vertex_coordinates%(restriction)s[3*vertex%(restriction)s1 + 2];
const double t%(restriction)s_length = std::sqrt(t%(restriction)s0*t%(restriction)s0 + t%(restriction)s1*t%(restriction)s1 + t%(restriction)s2*t%(restriction)s2);
t%(restriction)s0 /= t%(restriction)s_length;
t%(restriction)s1 /= t%(restriction)s_length;
t%(restriction)s2 /= t%(restriction)s_length;

// Subtract, the projection of (p2  - p0) onto (p2 - p1), from (p2 - p0)
const double ndott%(restriction)s = t%(restriction)s0*n%(restriction)s0 + t%(restriction)s1*n%(restriction)s1 + t%(restriction)s2*n%(restriction)s2;
n%(restriction)s0 -= ndott%(restriction)s*t%(restriction)s0;
n%(restriction)s1 -= ndott%(restriction)s*t%(restriction)s1;
n%(restriction)s2 -= ndott%(restriction)s*t%(restriction)s2;
const double n%(restriction)s_length = std::sqrt(n%(restriction)s0*n%(restriction)s0 + n%(restriction)s1*n%(restriction)s1 + n%(restriction)s2*n%(restriction)s2);

// Normalize
n%(restriction)s0 /= n%(restriction)s_length;
n%(restriction)s1 /= n%(restriction)s_length;
n%(restriction)s2 /= n%(restriction)s_length;
"""

_facet_normal_3D_1D = """
// Compute facet normal
double n%(restriction)s0 = 0.0;
double n%(restriction)s1 = 0.0;
double n%(restriction)s2 = 0.0;
if (facet%(restriction)s == 0)
{
  n%(restriction)s0 = vertex_coordinates%(restriction)s[0] - vertex_coordinates%(restriction)s[3];
  n%(restriction)s1 = vertex_coordinates%(restriction)s[1] - vertex_coordinates%(restriction)s[4];
  n%(restriction)s1 = vertex_coordinates%(restriction)s[2] - vertex_coordinates%(restriction)s[5];
}
else
{
  n%(restriction)s0 = vertex_coordinates%(restriction)s[3] - vertex_coordinates%(restriction)s[0];
  n%(restriction)s1 = vertex_coordinates%(restriction)s[4] - vertex_coordinates%(restriction)s[1];
  n%(restriction)s1 = vertex_coordinates%(restriction)s[5] - vertex_coordinates%(restriction)s[2];
}
const double n%(restriction)s_length = std::sqrt(n%(restriction)s0*n%(restriction)s0 + n%(restriction)s1*n%(restriction)s1 + n%(restriction)s2*n%(restriction)s2);
n%(restriction)s0 /= n%(restriction)s_length;
n%(restriction)s1 /= n%(restriction)s_length;
n%(restriction)s2 /= n%(restriction)s_length;
"""

_cell_volume_1D = """\
// Cell volume
const double volume%(restriction)s = std::abs(detJ%(restriction)s);"""

_cell_volume_2D = """\
// Cell volume
const double volume%(restriction)s = std::abs(detJ%(restriction)s)/2.0;"""

_cell_volume_2D_1D = """\
// Cell volume of interval in 2D
const double volume%(restriction)s = std::abs(detJ%(restriction)s);"""

_cell_volume_3D = """\
// Cell volume
const double volume%(restriction)s = std::abs(detJ%(restriction)s)/6.0;"""

_cell_volume_3D_1D = """\
// Cell volume of interval in 3D
const double volume%(restriction)s = std::abs(detJ%(restriction)s);"""

_cell_volume_3D_2D = """\
// Cell volume of triangle in 3D
const double volume%(restriction)s = std::abs(detJ%(restriction)s)/2.0;"""

_circumradius_1D = """\
// Compute circumradius; in 1D it is equal to half the cell length
const double circumradius%(restriction)s = std::abs(detJ%(restriction)s)/2.0;"""

_circumradius_2D = """\
// Compute circumradius of triangle in 2D
const double v1v2%(restriction)s  = std::sqrt((vertex_coordinates%(restriction)s[4] - vertex_coordinates%(restriction)s[2])*(vertex_coordinates%(restriction)s[4] - vertex_coordinates%(restriction)s[2]) + (vertex_coordinates%(restriction)s[5] - vertex_coordinates%(restriction)s[3])*(vertex_coordinates%(restriction)s[5] - vertex_coordinates%(restriction)s[3]) );
const double v0v2%(restriction)s  = std::sqrt(J%(restriction)s[3]*J%(restriction)s[3] + J%(restriction)s[1]*J%(restriction)s[1]);
const double v0v1%(restriction)s  = std::sqrt(J%(restriction)s[0]*J%(restriction)s[0] + J%(restriction)s[2]*J%(restriction)s[2]);

const double circumradius%(restriction)s = 0.25*(v1v2%(restriction)s*v0v2%(restriction)s*v0v1%(restriction)s)/(volume%(restriction)s);"""

_circumradius_2D_1D = """\
// Compute circumradius of interval in 3D (1/2 volume)
const double circumradius%(restriction)s = std::abs(detJ%(restriction)s)/2.0;"""

_circumradius_3D = """\
// Compute circumradius
const double v1v2%(restriction)s  = std::sqrt( (vertex_coordinates%(restriction)s[6] - vertex_coordinates%(restriction)s[3])*(vertex_coordinates%(restriction)s[6] - vertex_coordinates%(restriction)s[3]) + (vertex_coordinates%(restriction)s[7] - vertex_coordinates%(restriction)s[4])*(vertex_coordinates%(restriction)s[7] - vertex_coordinates%(restriction)s[4]) + (vertex_coordinates%(restriction)s[8] - vertex_coordinates%(restriction)s[5])*(vertex_coordinates%(restriction)s[8] - vertex_coordinates%(restriction)s[5]) );
const double v0v2%(restriction)s  = std::sqrt(J%(restriction)s[1]*J%(restriction)s[1] + J%(restriction)s[4]*J%(restriction)s[4] + J%(restriction)s[7]*J%(restriction)s[7]);
const double v0v1%(restriction)s  = std::sqrt(J%(restriction)s[0]*J%(restriction)s[0] + J%(restriction)s[3]*J%(restriction)s[3] + J%(restriction)s[6]*J%(restriction)s[6]);
const double v0v3%(restriction)s  = std::sqrt(J%(restriction)s[2]*J%(restriction)s[2] + J%(restriction)s[5]*J%(restriction)s[5] + J%(restriction)s[8]*J%(restriction)s[8]);
const double v1v3%(restriction)s  = std::sqrt( (vertex_coordinates%(restriction)s[9] - vertex_coordinates%(restriction)s[3])*(vertex_coordinates%(restriction)s[9] - vertex_coordinates%(restriction)s[3]) + (vertex_coordinates%(restriction)s[10] - vertex_coordinates%(restriction)s[4])*(vertex_coordinates%(restriction)s[10] - vertex_coordinates%(restriction)s[4]) + (vertex_coordinates%(restriction)s[11] - vertex_coordinates%(restriction)s[5])*(vertex_coordinates%(restriction)s[11] - vertex_coordinates%(restriction)s[5]) );
const double v2v3%(restriction)s  = std::sqrt( (vertex_coordinates%(restriction)s[9] - vertex_coordinates%(restriction)s[6])*(vertex_coordinates%(restriction)s[9] - vertex_coordinates%(restriction)s[6]) + (vertex_coordinates%(restriction)s[10] - vertex_coordinates%(restriction)s[7])*(vertex_coordinates%(restriction)s[10] - vertex_coordinates%(restriction)s[7]) + (vertex_coordinates%(restriction)s[11] - vertex_coordinates%(restriction)s[8])*(vertex_coordinates%(restriction)s[11] - vertex_coordinates%(restriction)s[8]) );
const  double la%(restriction)s   = v1v2%(restriction)s*v0v3%(restriction)s;
const  double lb%(restriction)s   = v0v2%(restriction)s*v1v3%(restriction)s;
const  double lc%(restriction)s   = v0v1%(restriction)s*v2v3%(restriction)s;
const  double s%(restriction)s    = 0.5*(la%(restriction)s+lb%(restriction)s+lc%(restriction)s);
const  double area%(restriction)s = std::sqrt(s%(restriction)s*(s%(restriction)s-la%(restriction)s)*(s%(restriction)s-lb%(restriction)s)*(s%(restriction)s-lc%(restriction)s));

const double circumradius%(restriction)s = area%(restriction)s / ( 6.0*volume%(restriction)s );"""

_circumradius_3D_1D = """\
// Compute circumradius of interval in 3D (1/2 volume)
const double circumradius%(restriction)s = std::abs(detJ%(restriction)s)/2.0;"""

_circumradius_3D_2D = """\
// Compute circumradius of triangle in 3D
const double v1v2%(restriction)s  = std::sqrt( (vertex_coordinates%(restriction)s[6] - vertex_coordinates%(restriction)s[3])*(vertex_coordinates%(restriction)s[6] - vertex_coordinates%(restriction)s[3]) + (vertex_coordinates%(restriction)s[7] - vertex_coordinates%(restriction)s[4])*(vertex_coordinates%(restriction)s[7] - vertex_coordinates%(restriction)s[4]) + (vertex_coordinates%(restriction)s[8] - vertex_coordinates%(restriction)s[5])*(vertex_coordinates%(restriction)s[8] - vertex_coordinates%(restriction)s[5]));
const double v0v2%(restriction)s = std::sqrt( J%(restriction)s[3]*J%(restriction)s[3] + J%(restriction)s[1]*J%(restriction)s[1] + J%(restriction)s[5]*J%(restriction)s[5]);
const double v0v1%(restriction)s = std::sqrt( J%(restriction)s[0]*J%(restriction)s[0] + J%(restriction)s[2]*J%(restriction)s[2] + J%(restriction)s[4]*J%(restriction)s[4]);

const double circumradius%(restriction)s = 0.25*(v1v2%(restriction)s*v0v2%(restriction)s*v0v1%(restriction)s)/(volume%(restriction)s);"""

_facet_area_1D = """\
// Facet area (FIXME: Should this be 0.0?)
const double facet_area = 1.0;"""

_facet_area_2D = """\
// Facet area
const double facet_area = det;"""

_facet_area_2D_1D = """\
// Facet area
const double facet_area = 1.0;"""

_facet_area_3D = """\
// Facet area (divide by two because 'det' is scaled by area of reference triangle)
const double facet_area = det/2.0;"""

_facet_area_3D_1D = """\
// Facet area
const double facet_area = 1.0;"""

_facet_area_3D_2D = """\
// Facet area
const double facet_area = det;"""

evaluate_basis_dofmap = """\
unsigned int element = 0;
unsigned int tmp = 0;
for (unsigned int j = 0; j < %d; j++)
{
  if (tmp +  dofs_per_element[j] > i)
  {
    i -= tmp;
    element = element_types[j];
    break;
  }
  else
    tmp += dofs_per_element[j];
}"""

_min_facet_edge_length_3D = """\
// Min edge length of facet
double min_facet_edge_length;
compute_min_facet_edge_length_tetrahedron_3d(min_facet_edge_length, facet%(restriction)s, vertex_coordinates%(restriction)s);
"""

_max_facet_edge_length_3D = """\
// Max edge length of facet
double max_facet_edge_length;
compute_max_facet_edge_length_tetrahedron_3d(max_facet_edge_length, facet%(restriction)s, vertex_coordinates%(restriction)s);
"""

# FIXME: This is dead slow because of all the new calls
# Used in evaluate_basis_derivatives. For second order derivatives in 2D it will
# generate the combinations: [(0, 0), (0, 1), (1, 0), (1, 1)] (i.e., xx, xy, yx, yy)
# which will also be the ordering of derivatives in the return value.
combinations_snippet = """\
// Declare two dimensional array that holds combinations of derivatives and initialise
unsigned int %(combinations)s[%(max_num_derivatives)s][%(max_degree)s];
for (unsigned int row = 0; row < %(max_num_derivatives)s; row++)
{
  for (unsigned int col = 0; col < %(max_degree)s; col++)
    %(combinations)s[row][col] = 0;
}

// Generate combinations of derivatives
for (unsigned int row = 1; row < %(num_derivatives)s; row++)
{
  for (unsigned int num = 0; num < row; num++)
  {
    for (unsigned int col = %(n)s-1; col+1 > 0; col--)
    {
      if (%(combinations)s[row][col] + 1 > %(dimension-1)s)
        %(combinations)s[row][col] = 0;
      else
      {
        %(combinations)s[row][col] += 1;
        break;
      }
    }
  }
}"""

def _transform_snippet(tdim, gdim):

    if tdim == gdim:
        _t = ""
        _g = ""
    else:
        _t = "_t"
        _g = "_g"

    # Matricize K_ij -> {K_ij}
    matrix = "{{" + "}, {".join([", ".join(["K[%d]" % (t*gdim + g)
                                            for g in range(gdim)])
                                 for t in range(tdim)]) + "}};\n\n"
    snippet = """\
// Compute inverse of Jacobian
const double %%(K)s[%d][%d] = %s""" % (tdim, gdim, matrix)

    snippet +="""// Declare transformation matrix
// Declare pointer to two dimensional array and initialise
double %%(transform)s[%%(max_g_deriv)s][%%(max_t_deriv)s];
for (unsigned int j = 0; j < %%(num_derivatives)s%(g)s; j++)
{
  for (unsigned int k = 0; k < %%(num_derivatives)s%(t)s; k++)
    %%(transform)s[j][k] = 1;
}

// Construct transformation matrix
for (unsigned int row = 0; row < %%(num_derivatives)s%(g)s; row++)
{
  for (unsigned int col = 0; col < %%(num_derivatives)s%(t)s; col++)
  {
    for (unsigned int k = 0; k < %%(n)s; k++)
      %%(transform)s[row][col] *= %%(K)s[%%(combinations)s%(t)s[col][k]][%%(combinations)s%(g)s[row][k]];
  }
}""" % {"t":_t, "g":_g}

    return snippet

# Codesnippets used in evaluate_dof
_map_onto_physical_1D = """\
// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X_%(i)d[%(j)s][0];
const double w1 = X_%(i)d[%(j)s][0];

// Compute affine mapping y = F(X)
y[0] = w0*vertex_coordinates[0] + w1*vertex_coordinates[1];"""

_map_onto_physical_2D = """\
// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X_%(i)d[%(j)s][0] - X_%(i)d[%(j)s][1];
const double w1 = X_%(i)d[%(j)s][0];
const double w2 = X_%(i)d[%(j)s][1];

// Compute affine mapping y = F(X)
y[0] = w0*vertex_coordinates[0] + w1*vertex_coordinates[2] + w2*vertex_coordinates[4];
y[1] = w0*vertex_coordinates[1] + w1*vertex_coordinates[3] + w2*vertex_coordinates[5];"""

_map_onto_physical_2D_1D = """\
// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X_%(i)d[%(j)s][0];
const double w1 = X_%(i)d[%(j)s][0];

// Compute affine mapping y = F(X)
y[0] = w0*vertex_coordinates[0] + w1*vertex_coordinates[2];
y[1] = w0*vertex_coordinates[1] + w1*vertex_coordinates[3];"""

_map_onto_physical_3D = """\
// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X_%(i)d[%(j)s][0] - X_%(i)d[%(j)s][1] - X_%(i)d[%(j)s][2];
const double w1 = X_%(i)d[%(j)s][0];
const double w2 = X_%(i)d[%(j)s][1];
const double w3 = X_%(i)d[%(j)s][2];

// Compute affine mapping y = F(X)
y[0] = w0*vertex_coordinates[0] + w1*vertex_coordinates[3] + w2*vertex_coordinates[6] + w3*vertex_coordinates[9];
y[1] = w0*vertex_coordinates[1] + w1*vertex_coordinates[4] + w2*vertex_coordinates[7] + w3*vertex_coordinates[10];
y[2] = w0*vertex_coordinates[2] + w1*vertex_coordinates[5] + w2*vertex_coordinates[8] + w3*vertex_coordinates[11];"""

_map_onto_physical_3D_1D = """\
// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X_%(i)d[%(j)s][0];
const double w1 = X_%(i)d[%(j)s][0];

// Compute affine mapping y = F(X)
y[0] = w0*vertex_coordinates[0] + w1*vertex_coordinates[3];
y[1] = w0*vertex_coordinates[1] + w1*vertex_coordinates[4];
y[2] = w0*vertex_coordinates[2] + w1*vertex_coordinates[5];"""

_map_onto_physical_3D_2D = """\
// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X_%(i)d[%(j)s][0] - X_%(i)d[%(j)s][1];
const double w1 = X_%(i)d[%(j)s][0];
const double w2 = X_%(i)d[%(j)s][1];

// Compute affine mapping y = F(X)
y[0] = w0*vertex_coordinates[0] + w1*vertex_coordinates[3] + w2*vertex_coordinates[6];
y[1] = w0*vertex_coordinates[1] + w1*vertex_coordinates[4] + w2*vertex_coordinates[7];
y[2] = w0*vertex_coordinates[2] + w1*vertex_coordinates[5] + w2*vertex_coordinates[8];
"""

_ip_coordinates_1D = """\
X%(num_ip)d[0] = %(name)s[%(ip)s][0]*vertex_coordinates%(restriction)s[0] + \
                 %(name)s[%(ip)s][1]*vertex_coordinates%(restriction)s[1];"""

_ip_coordinates_2D = """\
X%(num_ip)d[0] = %(name)s[%(ip)s][0]*vertex_coordinates%(restriction)s[0] + \
                 %(name)s[%(ip)s][1]*vertex_coordinates%(restriction)s[2] + %(name)s[%(ip)s][2]*vertex_coordinates%(restriction)s[4];
X%(num_ip)d[1] = %(name)s[%(ip)s][0]*vertex_coordinates%(restriction)s[1] + \
                 %(name)s[%(ip)s][1]*vertex_coordinates%(restriction)s[3] + %(name)s[%(ip)s][2]*vertex_coordinates%(restriction)s[5];"""

_ip_coordinates_3D = """\
X%(num_ip)d[0] = %(name)s[%(ip)s][0]*vertex_coordinates%(restriction)s[0] + \
                 %(name)s[%(ip)s][1]*vertex_coordinates%(restriction)s[3] + \
                 %(name)s[%(ip)s][2]*vertex_coordinates%(restriction)s[6] + \
                 %(name)s[%(ip)s][3]*vertex_coordinates%(restriction)s[9];
X%(num_ip)d[1] = %(name)s[%(ip)s][0]*vertex_coordinates%(restriction)s[1] + \
                 %(name)s[%(ip)s][1]*vertex_coordinates%(restriction)s[4] + \
                 %(name)s[%(ip)s][2]*vertex_coordinates%(restriction)s[7] + \
                 %(name)s[%(ip)s][3]*vertex_coordinates%(restriction)s[10];
X%(num_ip)d[2] = %(name)s[%(ip)s][0]*vertex_coordinates%(restriction)s[2] + \
                 %(name)s[%(ip)s][1]*vertex_coordinates%(restriction)s[5] + \
                 %(name)s[%(ip)s][2]*vertex_coordinates%(restriction)s[8] + \
                 %(name)s[%(ip)s][3]*vertex_coordinates%(restriction)s[11];"""

# Codesnippets used in evaluatebasis[|derivatives]
_map_coordinates_FIAT_interval = """\
// Get coordinates and map to the reference (FIAT) element
double X = (2.0*x[0] - vertex_coordinates[0] - vertex_coordinates[1]) / J[0];"""

_map_coordinates_FIAT_interval_in_2D = """\
// Get coordinates and map to the reference (FIAT) element
double X = 2*(std::sqrt(std::pow(x[0] - vertex_coordinates[0], 2) + std::pow(x[1] - vertex_coordinates[1], 2)) / detJ) - 1.0;"""

_map_coordinates_FIAT_interval_in_3D = """\
// Get coordinates and map to the reference (FIAT) element
double X = 2*(std::sqrt(std::pow(x[0] - vertex_coordinates[0], 2) + std::pow(x[1] - vertex_coordinates[1], 2) + std::pow(x[2] - vertex_coordinates[2], 2))/ detJ) - 1.0;"""

_map_coordinates_FIAT_triangle = """\
// Compute constants
const double C0 = vertex_coordinates[2] + vertex_coordinates[4];
const double C1 = vertex_coordinates[3] + vertex_coordinates[5];

// Get coordinates and map to the reference (FIAT) element
double X = (J[1]*(C1 - 2.0*x[1]) + J[3]*(2.0*x[0] - C0)) / detJ;
double Y = (J[0]*(2.0*x[1] - C1) + J[2]*(C0 - 2.0*x[0])) / detJ;"""

_map_coordinates_FIAT_triangle_in_3D = """\
const double b0 = vertex_coordinates[0];
const double b1 = vertex_coordinates[1];
const double b2 = vertex_coordinates[2];

// P_FFC = J^dag (p - b), P_FIAT = 2*P_FFC - (1, 1)
double X = 2*(K[0]*(x[0] - b0) + K[1]*(x[1] - b1) + K[2]*(x[2] - b2)) - 1.0;
double Y = 2*(K[3]*(x[0] - b0) + K[4]*(x[1] - b1) + K[5]*(x[2] - b2)) - 1.0;
"""

_map_coordinates_FIAT_tetrahedron = """\
// Compute constants
const double C0 = vertex_coordinates[9]  + vertex_coordinates[6] + vertex_coordinates[3]  - vertex_coordinates[0];
const double C1 = vertex_coordinates[10] + vertex_coordinates[7] + vertex_coordinates[4]  - vertex_coordinates[1];
const double C2 = vertex_coordinates[11] + vertex_coordinates[8] + vertex_coordinates[5]  - vertex_coordinates[2];

// Compute subdeterminants
const double d_00 = J[4]*J[8] - J[5]*J[7];
const double d_01 = J[5]*J[6] - J[3]*J[8];
const double d_02 = J[3]*J[7] - J[4]*J[6];
const double d_10 = J[2]*J[7] - J[1]*J[8];
const double d_11 = J[0]*J[8] - J[2]*J[6];
const double d_12 = J[1]*J[6] - J[0]*J[7];
const double d_20 = J[1]*J[5] - J[2]*J[4];
const double d_21 = J[2]*J[3] - J[0]*J[5];
const double d_22 = J[0]*J[4] - J[1]*J[3];

// Get coordinates and map to the reference (FIAT) element
double X = (d_00*(2.0*x[0] - C0) + d_10*(2.0*x[1] - C1) + d_20*(2.0*x[2] - C2)) / detJ;
double Y = (d_01*(2.0*x[0] - C0) + d_11*(2.0*x[1] - C1) + d_21*(2.0*x[2] - C2)) / detJ;
double Z = (d_02*(2.0*x[0] - C0) + d_12*(2.0*x[1] - C1) + d_22*(2.0*x[2] - C2)) / detJ;
"""

# Mappings to code snippets used by format These dictionaries accept
# as keys: first the topological dimension, and second the geometric
# dimension

facet_determinant = {1: {1: _facet_determinant_1D,
                         2: _facet_determinant_2D_1D,
                         3: _facet_determinant_3D_1D},
                     2: {2: _facet_determinant_2D,
                         3: _facet_determinant_3D_2D},
                     3: {3: _facet_determinant_3D}}

# Geometry related snippets
map_onto_physical = {1: {1: _map_onto_physical_1D,
                         2: _map_onto_physical_2D_1D,
                         3: _map_onto_physical_3D_1D},
                     2: {2: _map_onto_physical_2D,
                         3: _map_onto_physical_3D_2D},
                     3: {3: _map_onto_physical_3D}}

fiat_coordinate_map = {"interval": {1:_map_coordinates_FIAT_interval,
                                    2:_map_coordinates_FIAT_interval_in_2D,
                                    3:_map_coordinates_FIAT_interval_in_3D},
                       "triangle": {2:_map_coordinates_FIAT_triangle,
                                    3: _map_coordinates_FIAT_triangle_in_3D},
                       "tetrahedron": {3:_map_coordinates_FIAT_tetrahedron}}

transform_snippet = {"interval": {1: _transform_snippet(1, 1),
                                  2: _transform_snippet(1, 2),
                                  3: _transform_snippet(1, 3)},
                     "triangle": {2: _transform_snippet(2, 2),
                                  3: _transform_snippet(2, 3)},
                     "tetrahedron": {3: _transform_snippet(3, 3)}}

ip_coordinates = {1: (3, _ip_coordinates_1D),
                  2: (10, _ip_coordinates_2D),
                  3: (21, _ip_coordinates_3D)}

# FIXME: Rename as in compute_jacobian _compute_foo_<shape>_<n>d

normal_direction = {1: {1: _normal_direction_1D,
                        2: _normal_direction_2D_1D,
                        3: _normal_direction_3D_1D},
                    2: {2: _normal_direction_2D,
                        3: _normal_direction_3D_2D},
                    3: {3: _normal_direction_3D}}

facet_normal = {1: {1: _facet_normal_1D,
                    2: _facet_normal_2D_1D,
                    3: _facet_normal_3D_1D},
                2: {2: _facet_normal_2D,
                    3: _facet_normal_3D_2D},
                3: {3: _facet_normal_3D}}

cell_volume = {1: {1: _cell_volume_1D,
                   2: _cell_volume_2D_1D,
                   3: _cell_volume_3D_1D},
               2: {2: _cell_volume_2D,
                   3: _cell_volume_3D_2D},
               3: {3: _cell_volume_3D}}

circumradius = {1: {1: _circumradius_1D,
                    2: _circumradius_2D_1D,
                    3: _circumradius_3D_1D},
                2: {2: _circumradius_2D,
                    3: _circumradius_3D_2D},
                3: {3: _circumradius_3D}}

facet_area = {1: {1: _facet_area_1D,
                  2: _facet_area_2D_1D,
                  3: _facet_area_3D_1D},
              2: {2: _facet_area_2D,
                  3: _facet_area_3D_2D},
              3: {3: _facet_area_3D}}

min_facet_edge_length = {3: {3: _min_facet_edge_length_3D}}

max_facet_edge_length = {3: {3: _max_facet_edge_length_3D}}

# Code snippets for runtime quadrature (calling evaluate_basis)

eval_basis_decl = """\
std::vector<std::vector<double> > %(prefix)s(num_quadrature_points);"""

eval_basis = """\
// Get current quadrature point and compute values of basis function derivatives
const double* x = quadrature_points + ip*%(gdim)s;
static double values[%(num_vals)s];
const int cell_orientation = 0; // cell orientation currently not supported
evaluate_basis_all(values, x, vertex_coordinates, cell_orientation);"""

eval_basis_copy = """\

// Copy values to table %(prefix)s
%(prefix)s[ip].resize(%(num_vals)s);
std::copy(values, values + %(num_vals)s, %(prefix)s[ip].begin());
"""

eval_derivs_decl = """\
std::vector<std::vector<double> > %(prefix)s_D%(d)s(num_quadrature_points);"""

eval_derivs = """\
// Get current quadrature point and compute values of basis function derivatives
const double* x = quadrature_points + ip*%(gdim)s;
static double values[%(num_vals)s];
const int cell_orientation = 0; // cell orientation currently not supported
evaluate_basis_derivatives_all(%(n)s, values, x, vertex_coordinates, cell_orientation);"""

eval_derivs_copy = """\

// Copy values to table %(prefix)s_D%(d)s
%(prefix)s_D%(d)s[ip].resize(%(num_vals)s);
for (unsigned int i = 0; i < %(num_vals)s; i++)
  %(prefix)s_D%(d)s[ip][i] = values[%(offset)s + i*%(stride)s];"""
