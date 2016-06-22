BOOST_DIR="${HOME}/CompiledLibs/boost_1_59_0"
PYTHON_VERSION_S=3
PYTHON_VERSION_M=5

cmake .. \
-DCMAKE_C_COMPILER=${HOME}/CompiledLibs/clang-3.8.0-16.04-prebuilt/bin/clang                    \
-DCMAKE_INSTALL_RPATH="${HOME}/Kratos/libs"                                                     \
-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=TRUE                                                        \
-DCMAKE_CXX_COMPILER=${HOME}/CompiledLibs/clang-3.8.0-16.04-prebuilt/bin/clang++                \
-DCMAKE_C_FLAGS="${CMAKE_C_FLAGS} -msse3 -fopenmp"                                              \
-DCMAKE_CXX_FLAGS="${CMAKE_CXX_FLAGS} -msse3 -std=c++11 -fopenmp"                               \
-DBOOST_ROOT="${BOOST_DIR}"                                                                     \
-DPYTHON_LIBRARY="/usr/lib/python${PYTHON_VERSION_S}.${PYTHON_VERSION_M}/config-${PYTHON_VERSION_S}.${PYTHON_VERSION_M}m-x86_64-linux-gnu/libpython${PYTHON_VERSION_S}.${PYTHON_VERSION_M}m.so"                            \
-DPYTHON_INCLUDE_DIR="/usr/include/python${PYTHON_VERSION_S}.${PYTHON_VERSION_M}"               \
-DINCOMPRESSIBLE_FLUID_APPLICATION=ON                                                           \
-DMESHING_APPLICATION=ON                                                                        \
-DEXTERNAL_SOLVERS_APPLICATION=ON                                                               \
-DPFEM_APPLICATION=ON                                                                           \
-DSTRUCTURAL_APPLICATION=ON                                                                     \
-DCONVECTION_DIFFUSION_APPLICATION=ON                                                           \
-DFLUID_DYNAMICS_APPLICATION=ON                                                                 \
-DALE_APPLICATION=ON                                                                            \
-DFSI_APPLICATION=ON                                                                            \
-DDEM_APPLICATION=ON                                                                            \
-DSWIMMING_DEM_APPLICATION=ON                                                                   \
-DSOLID_MECHANICS_APPLICATION=ON                                                                \
-DPFEM_SOLID_MECHANICS_APPLICATION=ON                                                           \
-DTHERMO_MECHANICAL_APPLICATION=ON                                                              \
-DOPENCL_APPLICATION=OFF                                                                        \
-DMIXED_ELEMENT_APPLICATION=ON                                                                  \
-DMKL_SOLVERS_APPLICATION=OFF                                                                   \
-DSTRUCTURAL_MECHANICS_APPLICATION=ON                                                           \
-DMKLSOLVER_INCLUDE_DIR=\"UNSET\"                                                               \
-DMKLSOLVER_LIB_DIR=\"UNSET\"                                                                   \
-DMETIS_APPLICATION=OFF                                                                         \
-DPARMETIS_ROOT_DIR=\"UNSET\"                                                                   \
-DTRILINOS_APPLICATION=OFF                                                                      \
-DTRILINOS_ROOT=\"UNSET\"                                                                       \
-DINSTALL_EMBEDDED_PYTHON=ON                                                                    \
