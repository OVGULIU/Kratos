from __future__ import print_function, absolute_import, division  # makes backward compatible with python 2.6 and 2.7

from KratosMultiphysics.CoSimulationApplication.co_simulation_tools import ImportDataStructure
from KratosMultiphysics.CoSimulationApplication.co_simulation_analysis import CoSimulationAnalysis

if __name__ == '__main__':
    from sys import argv

    if len(argv) != 2:
        err_msg = 'Wrong number of input arguments!\n'
        err_msg += 'Use this script in the following way:\n'
        err_msg += '    "python MainKratos.py <cosim-parameter-file>.json"\n'
        raise Exception(err_msg)

    parameter_file_name = argv[1]
    cs_data_structure = ImportDataStructure(parameter_file_name)

    # Now we import actual parameters from the cs_data_structure
    with open(parameter_file_name, 'r') as parameter_file:
        parameters = cs_data_structure.Parameters(parameter_file.read())

    simulation = CoSimulationAnalysis(parameters)
    simulation.Run()

