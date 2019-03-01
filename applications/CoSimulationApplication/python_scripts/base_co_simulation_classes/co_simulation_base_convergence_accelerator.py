from __future__ import print_function, absolute_import, division  # makes these scripts backward compatible with python 2.6 and 2.7

# Other imports
import KratosMultiphysics.CoSimulationApplication.co_simulation_tools as tools


##
#  IMPORTANT : This is a BASE CLASS
#               Please do not change any thing in this class.
#
# This Class servers as a base class for all the Convergence accelerator techniques
# used in co simulation.
class CoSimulationBaseConvergenceAccelerator(object):
    def __init__(self, settings, solver):
        self.solver = solver
        self.settings = settings
        self.echo_level = 0

    ## Initialize : Initialize function for the accelerator class. Necessary
    #               initialization of the variables and objects to be done here.
    #  @param self                      The object pointer.
    def Initialize(self):
        pass

    ## Finalize :  Initialize function for the accelerator class.
    #               finalization of the variables and objects to be done here.
    #  @param self                      The object pointer.
    def Finalize(self):
        pass

    ## InitializeSolutionStep : Called once in the beginning of the solution step
    #

    def InitializeSolutionStep(self):
        pass

    ## FinalizeSolutionStep : Called once at the end of the solution step
    #

    def FinalizeSolutionStep(self):
        pass

    ## FinalizeNonLinearIteration : Function initializes the non linear iteration (coupling iteration)
    #                               Called at the beginning of the nonlinear iteration (coupling iteration)
    #

    def InitializeNonLinearIteration(self):
        raise NotImplementedError(tools.bcolors.FAIL + "CoSimulationBaseConvergenceAccelerator : Calling InitializeNonLinearIteration function !" + tools.bcolors.ENDC)

    ## FinalizeNonLinearIteration : Function finalizes the non linear iteration (coupling iteration)
    #                               Called at the end of the nonlinear iteration (coupling iteration)
    #

    def FinalizeNonLinearIteration(self):
        raise NotImplementedError(tools.bcolors.FAIL + "CoSimulationBaseConvergenceAccelerator : Calling FinalizeNonLinearIteration function !" + tools.bcolors.ENDC)

    ## ComputeUpdate : Function to compute the update for the fields. Should be called during the nonlinear (coupling iteration).
    #

    def ComputeUpdate(self):
        raise NotImplementedError(tools.bcolors.FAIL + "CoSimulationBaseConvergenceAccelerator : Calling ComputeUpdate function !" + tools.bcolors.ENDC)

    ## PrintInfo : Function to print the information of the convergence accelerator
    #

    def PrintInfo(self):
        raise NotImplementedError(tools.bcolors.FAIL + "CoSimulationBaseConvergenceAccelerator : Calling PrintInfo function !" + tools.bcolors.ENDC)

    ## SetEchoLevel : Function to set the echo_level of the convergence accelerator
    #

    #  @param level           int : echo level to be set
    def SetEchoLevel(self, level):
        self.echo_level = level

    ## Check : Function to Check the setup of the convergence accelerator
    #

    def Check(self):
        raise NotImplementedError(tools.bcolors.FAIL + "CoSimulationBaseConvergenceAccelerator : Calling Check function !" + tools.bcolors.ENDC)

    ## _Name : Function to get the name of the convergence accelerator
    #

    def _Name(self):
        raise NotImplementedError(tools.bcolors.FAIL + "CoSimulationBaseConvergenceAccelerator : Calling _Name function !" + tools.bcolors.ENDC)