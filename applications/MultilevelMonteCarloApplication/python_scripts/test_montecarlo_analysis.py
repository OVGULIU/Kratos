from __future__ import absolute_import, division #makes KratosMultiphysics backward compatible with python 2.6 and 2.7
import numpy as np
import time
import copy

# Importing the Kratos Library
import KratosMultiphysics

# Import applications
import KratosMultiphysics.ConvectionDiffusionApplication as KratosConvDiff

# Avoid printing of Kratos informations
KratosMultiphysics.Logger.GetDefaultOutput().SetSeverity(KratosMultiphysics.Logger.Severity.WARNING) # avoid printing of Kratos things

# Importing the base class
from analysis_stage import AnalysisStage

# Import variables class
from test_cmlmc_utilities import StatisticalVariable

# Import cpickle to pickle the serializer
try:
    import cpickle as pickle  # Use cPickle on Python 2.7
except ImportError:
    import pickle


'''Adapt the following class depending on the problem, deriving the MonteCarloAnalysis class from the problem of interest'''

'''This Analysis Stage implementation solves the elliptic PDE in (0,1)^2 with zero Dirichlet boundary conditions
-lapl(u) = xi*f,    f= -432*x*(x-1)*y*(y-1)
                    f= -432*(x**2+y**2-x-y)
where xi is a Beta(2,6) random variable, and computes statistic of the QoI
Q = int_(0,1)^2 u(x,y)dxdy
more details in Section 5.2 of [PKN17]

References:
[PKN17] M. Pisaroni; S. Krumscheid; F. Nobile : Quantifying uncertain system outputs via the multilevel Monte Carlo method - Part I: Central moment estimation; MATHICSE technical report no. 23.2017.
'''
class MonteCarloAnalysis(AnalysisStage):
    '''Main analysis stage for Monte Carlo simulations'''
    def __init__(self,input_model,input_parameters,sample):
        self.sample = sample
        super(MonteCarloAnalysis,self).__init__(input_model,input_parameters)
        self._GetSolver().main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.NODAL_AREA)

    def _CreateSolver(self):
        import convection_diffusion_stationary_solver
        return convection_diffusion_stationary_solver.CreateSolver(self.model,self.project_parameters["solver_settings"])
    
    def _GetSimulationName(self):
        return "Monte Carlo Analysis"

    '''Introduce here the stochasticity in the right hand side defining the forcing function and apply the stochastic contribute'''
    def ModifyInitialProperties(self):
        for node in self.model.GetModelPart("MLMCLaplacianModelPart").Nodes:
            coord_x = node.X
            coord_y = node.Y
            # forcing = -432.0 * coord_x * (coord_x - 1) * coord_y * (coord_y - 1)
            forcing = -432.0 * (coord_x**2 + coord_y**2 - coord_x - coord_y) # this forcing presents an analytical solution
            node.SetSolutionStepValue(KratosMultiphysics.HEAT_FLUX,forcing*self.sample)


##################################################
######## END OF CLASS MONTECARLOANALYSIS #########
##################################################


'''
function generating the random sample
here the sample has a beta distribution with parameters alpha = 2.0 and beta = 6.0
'''
def GenerateSample():
    alpha = 2.0
    beta = 6.0
    number_samples = 1
    sample = np.random.beta(alpha,beta,number_samples)
    return sample


'''
function evaluating the QoI of the problem: int_{domain} TEMPERATURE(x,y) dx dy
right now we are using the midpoint rule to evaluate the integral: improve!
'''
def EvaluateQuantityOfInterest(simulation):
    """here we evaluate the QoI of the problem: int_{domain} SOLUTION(x,y) dx dy
    we use the midpoint rule to evaluate the integral"""
    KratosMultiphysics.CalculateNodalAreaProcess(simulation._GetSolver().main_model_part,2).Execute()
    Q = 0.0
    for node in simulation._GetSolver().main_model_part.Nodes:
        Q = Q + (node.GetSolutionStepValue(KratosMultiphysics.NODAL_AREA)*node.GetSolutionStepValue(KratosMultiphysics.TEMPERATURE))
        #print("NODAL AREA = ",node.GetSolutionStepValue(KratosMultiphysics.NODAL_AREA),"NODAL SOLUTION = ",node.GetSolutionStepValue(KratosMultiphysics.TEMPERATURE),"CURRENT Q = ",Q)
    return Q


'''
function executing the problem
input:
        model       : serialization of the model
        parameters  : serialization of the Project Parameters
output:
        QoI         : Quantity of Interest
'''
def ExecuteMonteCarlo_Task(pickled_model, pickled_parameters):
    '''overwrite the old model serializer with the unpickled one'''
    model_serializer = pickle.loads(pickled_model)
    current_model = KratosMultiphysics.Model()
    model_serializer.Load("ModelSerialization",current_model)
    del(model_serializer)
    '''overwrite the old parameters serializer with the unpickled one'''
    serialized_parameters = pickle.loads(pickled_parameters)
    current_parameters = KratosMultiphysics.Parameters()
    serialized_parameters.Load("ParametersSerialization",current_parameters)
    del(serialized_parameters)
    sample = GenerateSample()
    simulation = MonteCarloAnalysis(current_model,current_parameters,sample)
    simulation.Run()
    QoI = EvaluateQuantityOfInterest(simulation)
    return QoI


'''
function executing the problem for sample = 1.0
input:
        model       : serialization of the model
        parameters  : serialization of the Project Parameters
output:
        ExactExpectedValueQoI : Quantity of Interest for sample = 1.0
OBSERVATION: here we multiply by 0.25 because it is the mean value of beta(2,6)
'''
def ExecuteExactMonteCarlo_Task(pickled_model, pickled_parameters):
    '''overwrite the old model serializer with the unpickled one'''
    model_serializer = pickle.loads(pickled_model)
    current_model = KratosMultiphysics.Model()
    model_serializer.Load("ModelSerialization",current_model)
    del(model_serializer)
    '''overwrite the old parameters serializer with the unpickled one'''
    serialized_parameters = pickle.loads(pickled_parameters)
    current_parameters = KratosMultiphysics.Parameters()
    serialized_parameters.Load("ParametersSerialization",current_parameters)
    del(serialized_parameters)
    sample = 1.0
    simulation = MonteCarloAnalysis(current_model,current_parameters,sample)
    simulation.Run()
    ExactExpectedValueQoI = 0.25 * EvaluateQuantityOfInterest(simulation)
    return ExactExpectedValueQoI


'''
function executing the refinement of the problem
input:
        pickled_model_coarse : serialization of the model with coarser model part
        pickled_parameters   : serialization of the Project Parameters
        min_size             : minimum size of the refined model part
        max_size             : maximum size of the refined mesh
output:
        QoI                   : Quantity of Interest
        pickled_model_refined : serialization of the model with refined model part
'''
def ExecuteRefinement_Task(pickled_model_coarse, pickled_parameters, min_size, max_size):
    sample = GenerateSample()
    '''overwrite the old model serializer with the unpickled one'''
    model_serializer_coarse = pickle.loads(pickled_model_coarse)
    model_coarse = KratosMultiphysics.Model()
    model_serializer_coarse.Load("ModelSerialization",model_coarse)
    del(model_serializer_coarse)
    '''overwrite the old parameters serializer with the unpickled one'''
    serialized_parameters = pickle.loads(pickled_parameters)
    parameters_refinement = KratosMultiphysics.Parameters()
    serialized_parameters.Load("ParametersSerialization",parameters_refinement)
    del(serialized_parameters)
    simulation_coarse = MonteCarloAnalysis(model_coarse,parameters_refinement,sample)
    simulation_coarse.Run()
    QoI =  EvaluateQuantityOfInterest(simulation_coarse)
    '''refine'''
    model_refined = refinement.compute_refinement_from_analysisstage_object(simulation_coarse,min_size,max_size)    
    '''initialize'''
    simulation = MonteCarloAnalysis(model_refined,parameters_refinement,sample)
    simulation.Initialize()
    '''serialize model and pickle it'''
    serialized_model = KratosMultiphysics.StreamSerializer()
    serialized_model.Save("ModelSerialization",simulation.model)
    pickled_model_refined = pickle.dumps(serialized_model, 2)
    return QoI,pickled_model_refined


'''
function serializing and pickling the model and the parameters of the problem
the idea is the following:
i)   from Model/Parameters Kratos object to StreamSerializer Kratos object
ii)  from StreamSerializer Kratos object to pickle string
iii) from pickle string to StreamSerializer Kratos object
iv)  from StreamSerializer Kratos object to Model/Parameters Kratos object
input:
        parameter_file_name   : path of the Project Parameters file
output:
        pickled_model      : model serializaton
        pickled_parameters : project parameters serialization
'''
def SerializeModelParameters_Task(parameter_file_name):
    with open(parameter_file_name,'r') as parameter_file:
        parameters = KratosMultiphysics.Parameters(parameter_file.read())
    local_parameters = parameters
    model = KratosMultiphysics.Model()
    # local_parameters["solver_settings"]["model_import_settings"]["input_filename"].SetString(model_part_file_name[:-5])
    fake_sample = 1.0
    simulation = MonteCarloAnalysis(model,local_parameters,fake_sample)
    simulation.Initialize()
    serialized_model = KratosMultiphysics.StreamSerializer()
    serialized_model.Save("ModelSerialization",simulation.model)
    serialized_parameters = KratosMultiphysics.StreamSerializer()
    serialized_parameters.Save("ParametersSerialization",simulation.project_parameters)
    # pickle dataserialized_data
    pickled_model = pickle.dumps(serialized_model, 2) # second argument is the protocol and is NECESSARY (according to pybind11 docs)
    pickled_parameters = pickle.dumps(serialized_parameters, 2)
    return pickled_model, pickled_parameters


'''
function computing the relative error between the Multilevel Monte Carlo expected value and the exact expected value
input :
        AveragedMeanQoI       : Multilevel Monte Carlo expected value
        ExactExpectedValueQoI : exact expected value
output :
        relative_error        : relative error
'''
def CompareMean_Task(AveragedMeanQoI,ExactExpectedValueQoI):
    relative_error = abs((AveragedMeanQoI - ExactExpectedValueQoI)/ExactExpectedValueQoI)
    return relative_error