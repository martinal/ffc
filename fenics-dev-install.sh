#!/usr/bin/env bash
#
# Developer script for configure + build + rebuild.
#
# Notes:
#
# - This script is what most developers use to build/rebuild this package.
# - This script is common to all distutils-based FEniCS packages.
# - If this script is updated in one package, please propagate to the others!
#
# Environment variables:
#
# - $FENICS_DIR : controls installation directory $FENICS_DIR/$BRANCH
#               : defaults to $HOME/opt/fenics
# - $PROCS      : controls number of processors to use for build
#               : defaults to 6

# Check and set FENICS_DIR
if [ -z "${FENICS_DIR}" ]; then
    FENICS_DIR=${HOME}/opt/fenics
fi

# Get branch name
BRANCH=`(git symbolic-ref --short HEAD 2> /dev/null || git describe HEAD) | sed s:/:.:g`

# Set installation prefix
FENICS_INSTALL_PREFIX="${FENICS_DIR}/${BRANCH}"
echo "Installation prefix set to ${INSTALL_PREFIX}"

# Configure and install
python setup.py install --prefix=${FENICS_INSTALL_PREFIX}

# Write config file
CONFIG_FILE="${FENICS_DIR}/fenics-$BRANCH.conf"
rm -f ${CONFIG_FILE}
cat << EOF > ${CONFIG_FILE}
# FEniCS configuration file created by upd on $(date)
export FENICS_INSTALL_PREFIX=${FENICS_INSTALL_PREFIX}
export PATH=\${FENICS_INSTALL_PREFIX}/bin:\$PATH
export PYTHONPATH=\${FENICS_INSTALL_PREFIX}/lib/python2.7/site-packages:\$PYTHONPATH
export CMAKE_PREFIX_PATH=\${FENICS_INSTALL_PREFIX}:\$CMAKE_PREFIX_PATH
EOF

# Print information
echo
echo "- Installed branch '${BRANCH}' to ${FENICS_INSTALL_PREFIX}."
echo
echo "- Config file written to ${CONFIG_FILE}"
echo "  (source this file)."
echo