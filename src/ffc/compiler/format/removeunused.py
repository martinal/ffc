"Utility function for removing unused variables from a C++ code"

__author__ = "Anders Logg (logg@simula.no)"
__date__ = "2007-03-07 -- 2007-03-07"
__copyright__ = "Copyright (C) 2007 Anders Logg"
__license__  = "GNU GPL Version 2"

# FFC common modules
from ffc.common.debug import *

# Declarations to examine
types = [["double"], ["const", "double"]]

def remove_unused(code):
    """Remove unused variables from a given C++ code. This is useful
    when generating code that will be compiled with gcc and options
    -Wall -Werror, in which case gcc returns an error when seeing a
    variable declaration for a variable that is never used."""

    # Dictionary of (declaration_line, used_lines) for variables
    variables = {}

    # List of variable names (so we can search them in order)
    variable_names = []

    # Examine code line by line
    lines = code.split("\n")
    for line_number in range(len(lines)):

        # Split words
        line = lines[line_number]
        words = [word for word in line.split(" ") if not word == ""]

        # Remember line where variable is declared
        for type in [type for type in types if len(words) > len(type)]:
            variable_type = words[0:len(type)]
            variable_name = words[len(type)]
            if variable_type == type:
                variables[variable_name] = (line_number, [])
                if not variable_name in variable_names:
                    variable_names += [variable_name]

        # Mark line for used variables
        for variable_name in variables:
            (declaration_line, used_lines) = variables[variable_name]
            if variable_name in line and line_number > declaration_line:
                variables[variable_name] = (declaration_line, used_lines + [line_number])

    # Reverse the order of the variable names (to catch variables used
    # only by variables that are removed)
    variable_names.reverse()
    
    # Remove declarations that are not used (need to search backwards)
    removed_lines = []
    for variable_name in variable_names:
        (declaration_line, used_lines) = variables[variable_name]
        for line in removed_lines:
            if line in used_lines:
                used_lines.remove(line)
        if used_lines == []:
            debug("Removing unused variable: %s" % variable_name, 1)
            lines[declaration_line] = "// " + lines[declaration_line]
            removed_lines += [declaration_line]
        
    return "\n".join([line for line in lines if not line == None])