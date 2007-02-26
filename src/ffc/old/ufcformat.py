"Code generation for the UFC 1.0 format."

__author__ = "Anders Logg (logg@simula.no)"
__date__ = "2007-01-08 -- 2007-01-27"
__copyright__ = "Copyright (C) 2007 Anders Logg"
__license__  = "GNU GPL Version 2"

# FFC common modules
from util import *
from debug import *
from constants import *

# FFC format modules
from ufc import *

# Specify formatting for code generation
format = { "add": lambda l: " + ".join(l),
           "sum": lambda l: " + ".join(l), # FIXME: Remove
           "subtract": lambda l: " - ".join(l),
           "multiply": lambda l: "*".join(l),
           "multiplication": lambda l: "*".join(l), # FIXME: Remove
           "grouping": lambda s: "(%s)" % s,
           "determinant": "det",
           "floating point": lambda a: "%.15e" % a,
           "bool": lambda b: {True: "true", False: "false"}[b],
           "constant": lambda j: "c%d" % j,
           "coefficient table": lambda j, k: "c[%d][%d]" % (j, k),
           "coefficient": lambda j, k: "c%d_%d" % (j, k),
           "transform": lambda j, k, r: "%s.g%d%d" % (r, j, k),
           "reference tensor" : lambda j, i, a: None,
           "geometry tensor": lambda j, a: "G%d_%s" % (j, "_".join(["%d" % index for index in a])),
           "element tensor": lambda i, k: "block[%d]" % k,
           "tmp declaration": lambda j, k: "const real tmp%d_%d" % (j, k),
           "tmp access": lambda j, k: "tmp%d_%d" % (j, k),
           "dofs": lambda i: "dofs[%d]" % i,
           "entity index": lambda d, i: "c.entity_indices[%d][%d]" % (d, i),
           "num entities": lambda dim : "m.num_entities[%d]" % dim,
           "offset declaration": "unsigned int offset",
           "offset access": "offset",
           "cell shape": lambda i: {1: "ufc::line", 2: "ufc::triangle", 3: "ufc::tetrahedron"}[i]}

def init(options):
    "Initialize code generation for the UFC 1.0 format."
    pass
    
def write(code, options):
    "Generate code for the UFC 1.0 format."
    debug("Generating code for UFC 1.0")

    # Set prefix
    prefix = code["name"].lower()

    # Generate file header
    output = ""
    output += __generate_header(prefix, options)
    output += "\n"

    # Generate code for ufc::finite_element(s)
    for i in range(code["num_arguments"]):
        output += __generate_finite_element(code[("finite_element", i)], options, prefix, i)
        output += "\n"

    # Generate code for ufc::dof_map(s)
    for i in range(code["num_arguments"]):
        output += __generate_dof_map(code[("dof_map", i)], options, prefix, i)
        output += "\n"

    # Generate code for ufc::cell_integral
    output += __generate_cell_integral(prefix, options)
    output += "\n"

    # Generate code for ufc::exterior_facet_integral
    output += __generate_exterior_facet_integral(prefix, options)
    output += "\n"
    
    # Generate code for ufc::cell_integral
    output += __generate_interior_facet_integral(prefix, options)
    output += "\n"

    # Generate code for ufc::form
    output += __generate_form(code["form"], options, prefix, code["num_arguments"])
    output += "\n"
    
    # Generate code for footer
    output += __generate_footer(prefix, options)

    # Write file
    filename = "%s_ufc.h" % prefix
    file = open(filename, "w")
    file.write(output)
    file.close()
    debug("Output written to " + filename)

def __generate_header(prefix, options):
    "Generate file header"

    # Check if BLAS is required
    if options["blas"]:
        blas_include = "\n#include <cblas.h>"
        blas_warning = "\n// Warning: This code was generated with '-f blas' and requires cblas.h."
    else:
        blas_include = ""
        blas_warning = ""
        
    return """\
// This code conforms with the UFC specification version 1.0.
//
// This code was automatically generated by FFC version %s.%s

#ifndef __%s_H
#define __%s_H

#include <ufc.h>%s
""" % (FFC_VERSION, blas_warning, prefix.upper(), prefix.upper(), blas_include)

def __generate_footer(prefix, options):
    "Generate file footer"
    return """\
#endif
"""

def __generate_finite_element(code, options, prefix, i):
    "Generate (modify) code for ufc::finite_element"

    ufc_code = {}

    # Set class name
    ufc_code["classname"] = "%s_finite_element_%d" % (prefix, i)

    # Generate code for members
    ufc_code["members"] = ""

    # Generate code for constructor
    ufc_code["constructor"] = "// Do nothing"

    # Generate code for destructor
    ufc_code["destructor"] = "// Do nothing"

    # Generate code for signature
    ufc_code["signature"] = "return \"%s\";" % code["signature"]

    # Generate code for cell_shape
    ufc_code["cell_shape"] = "return %s;" % code["cell_shape"]
    
    # Generate code for space_dimension
    ufc_code["space_dimension"] = "return %s;" % code["space_dimension"]

    # Generate code for value_rank
    ufc_code["value_rank"] = "return %s;" % code["value_rank"]

    # Generate code for value_dimension
    ufc_code["value_dimension"] = __generate_switch("i", code["value_dimension"], "0")

    # Generate code for evaluate_basis
    ufc_code["evaluate_basis"] = "// Not implemented"

    # Generate code for evaluate_dof
    ufc_code["evaluate_dof"] = "// Not implemented\nreturn 0.0;"

    # Generate code for inperpolate_vertex_values
    ufc_code["interpolate_vertex_values"] = "// Not implemented"

    # Generate code for num_sub_elements
    ufc_code["num_sub_elements"] = "return %s;" % code["num_sub_elements"]

    # Generate code for sub_element
    num_sub_elements = eval(code["num_sub_elements"])
    if num_sub_elements == 1:
        cases = ["new %s()" % ufc_code["classname"]]
    else:
        cases = ["new %s_sub_element_%d()" % (ufc_code["classname"], i) for i in range(num_sub_elements)]
    ufc_code["create_sub_element"] = __generate_switch(i, cases, 0)

    return __generate_code(finite_element_combined, ufc_code)

def __generate_dof_map(code, options, prefix, i):
    "Generate code for ufc::dof_map"

    ufc_code = {}

    # Set class name
    ufc_code["classname"] = "%s_dof_map_%d" % (prefix, i)

    # Generate code for members
    ufc_code["members"] = "\nprivate:\n\n  unsigned int __global_dimension;\n"

    # Generate code for constructor
    ufc_code["constructor"] = "__global_dimension = 0;"

    # Generate code for destructor
    ufc_code["destructor"] = "// Do nothing"

    # Generate code for signature
    ufc_code["signature"] = "return \"%s\";" % code["signature"]

    # Generate code for needs_mesh_entities
    ufc_code["needs_mesh_entities"] = __generate_switch("d", code["needs_mesh_entities"], "false")

    # Generate code for init_mesh
    ufc_code["init_mesh"] = "__global_dimension = %s;\nreturn false;" % code["global_dimension"]

    # Generate code for init_cell
    ufc_code["init_cell"] = "// Do nothing"

    # Generate code for init_cell_finalize
    ufc_code["init_cell_finalize"] = "// Do nothing"

    # Generate code for global_dimension
    ufc_code["global_dimension"] = "return __global_dimension;"

    # Generate code for local dimension
    ufc_code["local_dimension"] = "return %s;" % code["local_dimension"]

    # Generate code for num_facet_dofs
    ufc_code["num_facet_dofs"] = "// Not implemented\nreturn 0;"

    # Generate code for tabulate_dofs
    ufc_code["tabulate_dofs"] = "\n".join("%s = %s;" % declaration for declaration in code["tabulate_dofs"])

    # Generate code for tabulate_facet_dofs
    ufc_code["tabulate_facet_dofs"] = "// Not implemented"

    return __generate_code(dof_map_combined, ufc_code)

def __generate_cell_integral(prefix, options):
    "Generate code for ufc::cell_integral"

    code = {}

    # Set class name
    code["classname"] = "%s_cell_integral" % prefix

    # Generate code for members
    code["members"] = ""

    # Generate code for constructor
    code["constructor"] = "// Do nothing"

    # Generate code for destructor
    code["destructor"] = "// Do nothing"

    # Generate code for tabulate_tensor
    code["tabulate_tensor"] = "// Not implemented"
    
    return __generate_code(cell_integral_combined, code)

def __generate_exterior_facet_integral(prefix, options):
    "Generate code for ufc::exterior_facet_integral"

    code = {}

    # Set class name
    code["classname"] = "%s_exterior_facet_integral" % prefix

    # Generate code for members
    code["members"] = ""

    # Generate code for constructor
    code["constructor"] = "// Do nothing"

    # Generate code for destructor
    code["destructor"] = "// Do nothing"

    # Generate code for tabulate_tensor
    code["tabulate_tensor"] = "// Not implemented"
    
    return __generate_code(exterior_facet_integral_combined, code)

def __generate_interior_facet_integral(prefix, options):
    "Generate code for ufc::interior_facet_integral"

    code = {}

    # Set class name
    code["classname"] = "%s_interior_facet_integral" % prefix

    # Generate code for members
    code["members"] = ""

    # Generate code for constructor
    code["constructor"] = "// Do nothing"

    # Generate code for destructor
    code["destructor"] = "// Do nothing"

    # Generate code for tabulate_tensor
    code["tabulate_tensor"] = "// Not implemented"
    
    return __generate_code(interior_facet_integral_combined, code)

def __generate_form(code, options, prefix, num_arguments):
    "Generate code for ufc::form"

    ufc_code = {}

    # Set class name
    ufc_code["classname"] = prefix

    # Generate code for members
    ufc_code["members"] = ""

    # Generate code for constructor
    ufc_code["constructor"] = "// Do nothing"

    # Generate code for destructor
    ufc_code["destructor"] = "// Do nothing"

    # Generate code for signature
    ufc_code["signature"] = "return \"%s\";" % code["signature"]

    # Generate code for rank
    ufc_code["rank"] = "return %s;" % code["rank"]

    # Generate code for num_coefficients
    ufc_code["num_coefficients"] = "return %s;" % code["num_coefficients"]

    # Generate code for create_finite_element
    cases = ["new %s_finite_element_%d()" % (prefix, i) for i in range(num_arguments)]
    ufc_code["create_finite_element"] = __generate_switch("i", cases, "0")

    # Generate code for create_dof_map
    cases = ["new %s_dof_map_%d()" % (prefix, i) for i in range(num_arguments)]
    ufc_code["create_dof_map"] = __generate_switch("i", cases, "0")

    # Generate code for cell_integral
    ufc_code["create_cell_integral"] = "// Not implemented\nreturn 0;"

    # Generate code for exterior_facet_integral
    ufc_code["create_exterior_facet_integral"] = "// Not implemented\nreturn 0;"

    # Generate code for interior_facet_integral
    ufc_code["create_interior_facet_integral"] = "// Not implemented\nreturn 0;"

    return __generate_code(form_combined, ufc_code)

def __generate_switch(variable, cases, default):
    "Generate switch statement from given variable and cases"

    # Special case: just one case
    if len(cases) == 1:
        return "return %s;" % cases[0]

    # Generate switch
    code = "switch ( %s )\n{\n" % variable
    for i in range(len(cases)):
        code += "case %d:\n  return %s;\n  break;\n" % (i, cases[i])
    code += "default:\n  return 0;\n}\n\nreturn %s;" % default
    return code

def __generate_code(format_string, code):
    "Generate code according to format string and code dictionary"

    # Fix indentation
    for key in code:
        if not key in ["classname", "members"]:
            code[key] = indent(code[key], 4)

    # Generate code
    return format_string % code