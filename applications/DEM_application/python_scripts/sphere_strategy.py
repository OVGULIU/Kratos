import sys
from KratosMultiphysics import *
from KratosMultiphysics.DEMApplication import *

def Var_Translator(variable):

    if (variable == "OFF" or variable == "0"):
        variable = 0
    else:
        variable = 1

    return variable

def AddVariables(model_part, Param):

    # KINEMATIC
    model_part.AddNodalSolutionStepVariable(DISPLACEMENT)
    model_part.AddNodalSolutionStepVariable(DELTA_DISPLACEMENT)
    model_part.AddNodalSolutionStepVariable(VELOCITY)
    model_part.AddNodalSolutionStepVariable(PARTICLE_ROTATION_ANGLE)
    model_part.AddNodalSolutionStepVariable(DELTA_ROTA_DISPLACEMENT)
    model_part.AddNodalSolutionStepVariable(ORIENTATION_REAL)
    model_part.AddNodalSolutionStepVariable(ORIENTATION_IMAG)
    model_part.AddNodalSolutionStepVariable(ANGULAR_VELOCITY)

    # FORCES
    model_part.AddNodalSolutionStepVariable(ELASTIC_FORCES)
    model_part.AddNodalSolutionStepVariable(TOTAL_FORCES)
    model_part.AddNodalSolutionStepVariable(DAMP_FORCES)
    model_part.AddNodalSolutionStepVariable(PARTICLE_MOMENT)
    model_part.AddNodalSolutionStepVariable(EXTERNAL_APPLIED_FORCE)

    # BASIC PARTICLE PROPERTIES
    model_part.AddNodalSolutionStepVariable(RADIUS)
    model_part.AddNodalSolutionStepVariable(NODAL_MASS)
    model_part.AddNodalSolutionStepVariable(SQRT_OF_MASS)
    model_part.AddNodalSolutionStepVariable(PARTICLE_DENSITY)
    model_part.AddNodalSolutionStepVariable(YOUNG_MODULUS)
    model_part.AddNodalSolutionStepVariable(POISSON_RATIO)
    model_part.AddNodalSolutionStepVariable(LN_OF_RESTITUTION_COEFF)
    model_part.AddNodalSolutionStepVariable(PARTICLE_FRICTION)

    # ROTATION RELATED PROPERTIES

    if (Var_Translator(Param.RotationOption)):
        model_part.AddNodalSolutionStepVariable(PARTICLE_INERTIA)
        model_part.AddNodalSolutionStepVariable(PARTICLE_MOMENT_OF_INERTIA)
        model_part.AddNodalSolutionStepVariable(PARTICLE_ROTATION_DAMP_RATIO)
        model_part.AddNodalSolutionStepVariable(ROLLING_FRICTION)

    # OTHER PROPERTIES
    model_part.AddNodalSolutionStepVariable(PARTICLE_MATERIAL)   # Colour defined in GiD
    model_part.AddNodalSolutionStepVariable(PARTICLE_CONTINUUM)  # Continuum group
    model_part.AddNodalSolutionStepVariable(REPRESENTATIVE_VOLUME)
    model_part.AddNodalSolutionStepVariable(MAX_INDENTATION)

    # LOCAL AXIS
    model_part.AddNodalSolutionStepVariable(EULER_ANGLES)

    # BOUNDARY SURFACE

    if (Param.LimitSurfaceOption > 0):
        model_part.AddNodalSolutionStepVariable(PARTICLE_SURFACE_CONTACT_FORCES_1)
    if (Param.LimitSurfaceOption > 1):        
        model_part.AddNodalSolutionStepVariable(PARTICLE_SURFACE_CONTACT_FORCES_2)
    if (Param.LimitSurfaceOption > 2):
        model_part.AddNodalSolutionStepVariable(PARTICLE_SURFACE_CONTACT_FORCES_3)
    if (Param.LimitSurfaceOption > 3):
        model_part.AddNodalSolutionStepVariable(PARTICLE_SURFACE_CONTACT_FORCES_4)
    if (Param.LimitSurfaceOption > 4):
        model_part.AddNodalSolutionStepVariable(PARTICLE_SURFACE_CONTACT_FORCES_5)

    if (Param.LimitCylinderOption > 0):
        model_part.AddNodalSolutionStepVariable(PARTICLE_CYLINDER_CONTACT_FORCES_1)
    if (Param.LimitCylinderOption > 1):
        model_part.AddNodalSolutionStepVariable(PARTICLE_CYLINDER_CONTACT_FORCES_2)
    if (Param.LimitCylinderOption > 2):
        model_part.AddNodalSolutionStepVariable(PARTICLE_CYLINDER_CONTACT_FORCES_3)
    if (Param.LimitCylinderOption > 3):
        model_part.AddNodalSolutionStepVariable(PARTICLE_CYLINDER_CONTACT_FORCES_4)
    if (Param.LimitCylinderOption > 4):
        model_part.AddNodalSolutionStepVariable(PARTICLE_CYLINDER_CONTACT_FORCES_5)
    
    # FLAGS
    model_part.AddNodalSolutionStepVariable(GROUP_ID)            # Differencied groups for plotting, etc..
    model_part.AddNodalSolutionStepVariable(ERASE_FLAG)

    # ONLY VISUALITZATION
    model_part.AddNodalSolutionStepVariable(EXPORT_ID)

    if (Var_Translator(Param.PostGroupId)):
        model_part.AddNodalSolutionStepVariable(EXPORT_GROUP_ID)

    print "Variables for the explicit solver added correctly"

def AddDofs(model_part):

    for node in model_part.Nodes:
        node.AddDof(DISPLACEMENT_X, REACTION_X);
        node.AddDof(DISPLACEMENT_Y, REACTION_Y);
        node.AddDof(DISPLACEMENT_Z, REACTION_Z);
        node.AddDof(VELOCITY_X, REACTION_X);
        node.AddDof(VELOCITY_Y, REACTION_Y);
        node.AddDof(VELOCITY_Z, REACTION_Z);
        node.AddDof(ANGULAR_VELOCITY_X, REACTION_X);
        node.AddDof(ANGULAR_VELOCITY_Y, REACTION_Y);
        node.AddDof(ANGULAR_VELOCITY_Z, REACTION_Z);

    print "DOFs for the DEM solution added correctly"

class ExplicitStrategy:

    def __init__(self, model_part, creator_destructor, Param):

        # Initialization of member variables

        # SIMULATION FLAGS        
        self.virtual_mass_option            = Var_Translator(Param.VirtualMassOption)
        self.critical_time_option           = Var_Translator(Param.AutoReductionOfTimeStepOption)
        self.trihedron_option               = Var_Translator(Param.TrihedronOption)
        self.rotation_option                = Var_Translator(Param.RotationOption)
        self.bounding_box_option            = Var_Translator(Param.BoundingBoxOption)
        self.fix_velocities                 = Var_Translator(Param.FixVelocitiesOption)
        self.limit_surface_option           = Param.LimitSurfaceOption
        self.limit_cylinder_option          = Param.LimitCylinderOption       
        self.clean_init_indentation_option  = Var_Translator(Param.CleanIndentationsOption)
        self.homogeneous_material_option    = Var_Translator(Param.HomogeneousMaterialOption)
        self.global_variables_option        = Var_Translator(Param.GlobalVariablesOption)
        self.non_linear_option              = Var_Translator(Param.NonLinearNormalElasticOption)
        self.contact_mesh_option            = Var_Translator(Param.ContactMeshOption)
        self.search_radius_extension        = Var_Translator(Param.SearchRadiusExtension)
        self.automatic_bounding_box_option  = Var_Translator(Param.AutomaticBoundingBoxOption)
        self.move_mesh_flag                 = True
        self.deactivate_search              = 0
        self.case_option                    = 3


        # MODEL
        self.model_part                      = model_part

        # BOUNDING_BOX
        self.enlargement_factor             = Param.BoundingBoxEnlargementFactor
        self.top_corner                     = Array3()
        self.bottom_corner                  = Array3()
        self.top_corner[0]                  = Param.BoundingBoxMaxX
        self.top_corner[0]                  = Param.BoundingBoxMaxY
        self.top_corner[0]                  = Param.BoundingBoxMaxZ
        self.bottom_corner[0]               = Param.BoundingBoxMinX
        self.bottom_corner[0]               = Param.BoundingBoxMinY
        self.bottom_corner[0]               = Param.BoundingBoxMinZ

        # BOUNDARY
        if (Param.LimitSurfaceOption > 0):
          self.surface_normal_dir_1           = Vector(3)
          self.surface_normal_dir_1[0]        = Param.SurfaceNormalDirX1
          self.surface_normal_dir_1[1]        = Param.SurfaceNormalDirY1
          self.surface_normal_dir_1[2]        = Param.SurfaceNormalDirZ1
          self.surface_point_coor_1           = Vector(3)
          self.surface_point_coor_1[0]        = Param.SurfacePointCoorX1
          self.surface_point_coor_1[1]        = Param.SurfacePointCoorY1
          self.surface_point_coor_1[2]        = Param.SurfacePointCoorZ1
          self.surface_friction_angle_1       = Param.SurfaceFrictionAngle1
        if (Param.LimitSurfaceOption > 1):
          self.surface_normal_dir_2           = Vector(3)
          self.surface_normal_dir_2[0]        = Param.SurfaceNormalDirX2
          self.surface_normal_dir_2[1]        = Param.SurfaceNormalDirY2
          self.surface_normal_dir_2[2]        = Param.SurfaceNormalDirZ2
          self.surface_point_coor_2           = Vector(3)
          self.surface_point_coor_2[0]        = Param.SurfacePointCoorX2
          self.surface_point_coor_2[1]        = Param.SurfacePointCoorY2
          self.surface_point_coor_2[2]        = Param.SurfacePointCoorZ2
          self.surface_friction_angle_2       = Param.SurfaceFrictionAngle2
        if (Param.LimitSurfaceOption > 2):
          self.surface_normal_dir_3           = Vector(3)
          self.surface_normal_dir_3[0]        = Param.SurfaceNormalDirX3
          self.surface_normal_dir_3[1]        = Param.SurfaceNormalDirY3
          self.surface_normal_dir_3[2]        = Param.SurfaceNormalDirZ3
          self.surface_point_coor_3           = Vector(3)
          self.surface_point_coor_3[0]        = Param.SurfacePointCoorX3
          self.surface_point_coor_3[1]        = Param.SurfacePointCoorY3
          self.surface_point_coor_3[2]        = Param.SurfacePointCoorZ3
          self.surface_friction_angle_3       = Param.SurfaceFrictionAngle3
        if (Param.LimitSurfaceOption > 3):
          self.surface_normal_dir_4           = Vector(3)
          self.surface_normal_dir_4[0]        = Param.SurfaceNormalDirX4
          self.surface_normal_dir_4[1]        = Param.SurfaceNormalDirY4
          self.surface_normal_dir_4[2]        = Param.SurfaceNormalDirZ4
          self.surface_point_coor_4           = Vector(3)
          self.surface_point_coor_4[0]        = Param.SurfacePointCoorX4
          self.surface_point_coor_4[1]        = Param.SurfacePointCoorY4
          self.surface_point_coor_4[2]        = Param.SurfacePointCoorZ4
          self.surface_friction_angle_4       = Param.SurfaceFrictionAngle4
        if (Param.LimitSurfaceOption > 4):
          self.surface_normal_dir_5           = Vector(3)
          self.surface_normal_dir_5[0]        = Param.SurfaceNormalDirX5
          self.surface_normal_dir_5[1]        = Param.SurfaceNormalDirY5
          self.surface_normal_dir_5[2]        = Param.SurfaceNormalDirZ5
          self.surface_point_coor_5           = Vector(3)
          self.surface_point_coor_5[0]        = Param.SurfacePointCoorX5
          self.surface_point_coor_5[1]        = Param.SurfacePointCoorY5
          self.surface_point_coor_5[2]        = Param.SurfacePointCoorZ5
          self.surface_friction_angle_5       = Param.SurfaceFrictionAngle5
          
        if (Param.LimitCylinderOption > 0):
          self.cylinder_velocity              = Param.CylinderVelocity
          self.cylinder_angular_velocity      = Param.CylinderAngularVelocity
          self.cylinder_initial_base_centre   = Vector(3)
          self.cylinder_initial_base_centre[0]= Param.CylinderInitialBaseCentreX
          self.cylinder_initial_base_centre[1]= Param.CylinderInitialBaseCentreY
          self.cylinder_initial_base_centre[2]= Param.CylinderInitialBaseCentreZ        			
          self.cylinder_axis_dir              = Vector(3)
          self.cylinder_axis_dir[0]           = Param.CylinderAxisX
          self.cylinder_axis_dir[1]           = Param.CylinderAxisY
          self.cylinder_axis_dir[2]           = Param.CylinderAxisZ
          self.cylinder_radius_1              = Param.CylinderRadius1
          self.cylinder_friction_angle_1      = Param.CylinderFrictionAngle1
        if (Param.LimitCylinderOption > 1):
          self.cylinder_radius_2              = Param.CylinderRadius2
          self.cylinder_friction_angle_2      = Param.CylinderFrictionAngle2
        if (Param.LimitCylinderOption > 2):
          self.cylinder_radius_3              = Param.CylinderRadius3
          self.cylinder_friction_angle_3      = Param.CylinderFrictionAngle3
        if (Param.LimitCylinderOption > 3):
          self.cylinder_radius_4              = Param.CylinderRadius4
          self.cylinder_friction_angle_4      = Param.CylinderFrictionAngle4
        if (Param.LimitCylinderOption > 4):
          self.cylinder_radius_5              = Param.CylinderRadius5
          self.cylinder_friction_angle_5      = Param.CylinderFrictionAngle5

        # GLOBAL PHYSICAL ASPECTS
        self.gravity                        = Vector(3)
        self.gravity[0]                     = Param.GravityX
        self.gravity[1]                     = Param.GravityY
        self.gravity[2]                     = Param.GravityZ

        # GLOBAL MATERIAL PROPERTIES
        self.nodal_mass_coeff               = Param.VirtualMassCoefficient
        self.magic_factor                   = Param.MagicFactor

        if (self.global_variables_option):
            self.global_kn                  = Param.GlobalKn
            self.global_kt                  = Param.GlobalKt

        if (Param.NormalForceCalculationType == "Linear"):
            self.force_calculation_type_id  = 0

        elif (Param.NormalForceCalculationType == "Hertz"):
            self.force_calculation_type_id  = 1

        else:

            raise 'Specified NormalForceCalculationType is not defined'

        if (self.non_linear_option):
            self.C1                         = Param.C1
            self.C2                         = Param.C2
            self.N1                         = Param.N1
            self.N2                         = Param.N2

        if (Param.NormalDampingType == "ViscDamp"):

            if (Param.TangentialDampingType == "ViscDamp"):
                self.damp_id                = 11

            else:
                self.damp_id                = 10
        else:

            if (Param.TangentialDampingType == "ViscDamp"):
                self.damp_id                = 1

            else:
                self.damp_id                = 0

        if (Param.RotaDampingType == "LocalDamp"):
            self.rota_damp_id               = 1

        elif (Param.RotaDampingType == "RollingFric"):
            self.rota_damp_id               = 2

        else:
            self.rota_damp_id               = 0

        self.tau_zero                       = Param.TauZero
        self.sigma_max                      = Param.SigmaMax
        self.sigma_min                      = Param.SigmaMin

        # PRINTING VARIABLES
        self.print_export_id                = Var_Translator(Param.PostExportId)
        self.print_group_id                 = Var_Translator(Param.PostGroupId)
        self.print_radial_displacement      = Var_Translator(Param.PostRadialDisplacement)

        # TIME RELATED PARAMETERS
        self.delta_time                     = Param.MaxTimeStep
        self.max_delta_time                 = Param.MaxTimeStep
        self.final_time                     = Param.FinalTime

        # RESOLUTION METHODS AND PARAMETERS

        if (Param.TimeStepsPerSearchStep < 1):

            raise 'Variable TimeStepsPerSearchStep must be an integer, grater or equal to 1. The current input value is ', Param.TimeStepsPerSearchStep

        elif (not isinstance(Param.TimeStepsPerSearchStep, int)):

            print 'Variable TimeStepsPerSearchStep is not an integer. Its input value is ', Param.TimeStepsPerSearchStep, 'Rounding up to ', int(Param.TimeStepsPerSearchStep)

            self.n_step_search              = int(Param.TimeStepsPerSearchStep)

        else:
            self.n_step_search              = int(Param.TimeStepsPerSearchStep)

        if (self.deactivate_search):
            self.n_step_search              = sys.maxint

        self.safety_factor                  = Param.DeltaTimeSafetyFactor # For critical time step

        # CREATOR-DESTRUCTOR
        self.creator_destructor             = creator_destructor

        b_box_low     = Array3()
        b_box_high    = Array3()
        b_box_low[0]  = Param.BoundingBoxMaxX
        b_box_low[1]  = Param.BoundingBoxMaxY
        b_box_low[2]  = Param.BoundingBoxMaxZ
        b_box_high[0] = Param.BoundingBoxMinX
        b_box_high[1] = Param.BoundingBoxMinY
        b_box_high[2] = Param.BoundingBoxMinZ

        self.creator_destructor.SetLowNode(b_box_low)
        self.creator_destructor.SetHighNode(b_box_high)

        if (self.automatic_bounding_box_option):
            self.creator_destructor.CalculateSurroundingBoundingBox(self.model_part, self.enlargement_factor)

        # STRATEGIES
        self.search_strategy                = OMP_DEMSearch()

        if (Param.IntegrationScheme == 'forward_euler'):
            self.time_scheme                = ForwardEulerScheme()

        elif (Param.IntegrationScheme == 'mid_point_rule'):
            self.time_scheme                = MidPointScheme()

        elif (Param.IntegrationScheme == 'const_average_acc'):
            self.time_scheme                = ConstAverageAccelerationScheme()

        else:

            print('Specified IntegrationScheme is not defined')

    ######################################################################

    def Initialize(self):

        # Setting ProcessInfo variables

        # SIMULATION FLAGS
        self.model_part.ProcessInfo.SetValue(VIRTUAL_MASS_OPTION, self.virtual_mass_option)
        self.model_part.ProcessInfo.SetValue(CRITICAL_TIME_OPTION, self.critical_time_option)
        self.model_part.ProcessInfo.SetValue(CASE_OPTION, self.case_option)
        self.model_part.ProcessInfo.SetValue(TRIHEDRON_OPTION, self.trihedron_option)
        self.model_part.ProcessInfo.SetValue(ROTATION_OPTION, self.rotation_option)
        self.model_part.ProcessInfo.SetValue(BOUNDING_BOX_OPTION, self.bounding_box_option)
        self.model_part.ProcessInfo.SetValue(INT_DUMMY_6, self.fix_velocities)
        self.model_part.ProcessInfo.SetValue(GLOBAL_VARIABLES_OPTION, self.global_variables_option)
        self.model_part.ProcessInfo.SetValue(UNIFORM_MATERIAL_OPTION, self.homogeneous_material_option)
        self.model_part.ProcessInfo.SetValue(NEIGH_INITIALIZED, 0);
        self.model_part.ProcessInfo.SetValue(TOTAL_CONTACTS, 0);
        self.model_part.ProcessInfo.SetValue(CLEAN_INDENT_OPTION, self.clean_init_indentation_option);

        # TOTAL NUMBER OF INITIALIZED ELEMENTS
        self.model_part.ProcessInfo.SetValue(NUM_PARTICLES_INITIALIZED, 0);

        # TOLERANCES
        self.model_part.ProcessInfo.SetValue(DISTANCE_TOLERANCE, 0);

        # BOUNDARY
        self.model_part.ProcessInfo.SetValue(LIMIT_SURFACE_OPTION, self.limit_surface_option)
        if (self.limit_surface_option > 0):
          self.model_part.ProcessInfo.SetValue(SURFACE_NORMAL_DIR_1, self.surface_normal_dir_1)
          self.model_part.ProcessInfo.SetValue(SURFACE_POINT_COOR_1, self.surface_point_coor_1)
          self.model_part.ProcessInfo.SetValue(SURFACE_FRICC_1, self.surface_friction_angle_1)
        if (self.limit_surface_option > 1):
          self.model_part.ProcessInfo.SetValue(SURFACE_NORMAL_DIR_2, self.surface_normal_dir_2)
          self.model_part.ProcessInfo.SetValue(SURFACE_POINT_COOR_2, self.surface_point_coor_2)
          self.model_part.ProcessInfo.SetValue(SURFACE_FRICC_2, self.surface_friction_angle_2)
        if (self.limit_surface_option > 2):
          self.model_part.ProcessInfo.SetValue(SURFACE_NORMAL_DIR_3, self.surface_normal_dir_3)
          self.model_part.ProcessInfo.SetValue(SURFACE_POINT_COOR_3, self.surface_point_coor_3)
          self.model_part.ProcessInfo.SetValue(SURFACE_FRICC_3, self.surface_friction_angle_3)
        if (self.limit_surface_option > 3):
          self.model_part.ProcessInfo.SetValue(SURFACE_NORMAL_DIR_4, self.surface_normal_dir_4)
          self.model_part.ProcessInfo.SetValue(SURFACE_POINT_COOR_4, self.surface_point_coor_4)
          self.model_part.ProcessInfo.SetValue(SURFACE_FRICC_4, self.surface_friction_angle_4)
        if (self.limit_surface_option > 4):
          self.model_part.ProcessInfo.SetValue(SURFACE_NORMAL_DIR_5, self.surface_normal_dir_5)
          self.model_part.ProcessInfo.SetValue(SURFACE_POINT_COOR_5, self.surface_point_coor_5)
          self.model_part.ProcessInfo.SetValue(SURFACE_FRICC_5, self.surface_friction_angle_5)
          
        self.model_part.ProcessInfo.SetValue(LIMIT_CYLINDER_OPTION, self.limit_cylinder_option)
        if (self.limit_cylinder_option > 0):
          self.model_part.ProcessInfo.SetValue(CYLINDER_VELOCITY, self.cylinder_velocity)
          self.model_part.ProcessInfo.SetValue(CYLINDER_ANGULAR_VELOCITY, self.cylinder_angular_velocity)
          self.model_part.ProcessInfo.SetValue(INITIAL_BASE_CYLINDER_CENTRE, self.cylinder_initial_base_centre)                   			
          self.model_part.ProcessInfo.SetValue(CYLINDER_AXIS_DIR, self.cylinder_axis_dir)
          self.model_part.ProcessInfo.SetValue(CYLINDER_RADIUS_1, self.cylinder_radius_1)
          self.model_part.ProcessInfo.SetValue(CYLINDER_FRICC_1, self.cylinder_friction_angle_1)
        if (self.limit_cylinder_option > 1):
          self.model_part.ProcessInfo.SetValue(CYLINDER_RADIUS_2, self.cylinder_radius_2)
          self.model_part.ProcessInfo.SetValue(CYLINDER_FRICC_2, self.cylinder_friction_angle_2)
        if (self.limit_cylinder_option > 2):
          self.model_part.ProcessInfo.SetValue(CYLINDER_RADIUS_3, self.cylinder_radius_3)
          self.model_part.ProcessInfo.SetValue(CYLINDER_FRICC_3, self.cylinder_friction_angle_3)
        if (self.limit_cylinder_option > 3):
          self.model_part.ProcessInfo.SetValue(CYLINDER_RADIUS_4, self.cylinder_radius_4)
          self.model_part.ProcessInfo.SetValue(CYLINDER_FRICC_4, self.cylinder_friction_angle_4)
        if (self.limit_cylinder_option > 4):
          self.model_part.ProcessInfo.SetValue(CYLINDER_RADIUS_5, self.cylinder_radius_5)
          self.model_part.ProcessInfo.SetValue(CYLINDER_FRICC_5, self.cylinder_friction_angle_5)

        # GLOBAL PHISICAL ASPECTS
        self.model_part.ProcessInfo.SetValue(GRAVITY, self.gravity)
        self.model_part.ProcessInfo.SetValue(DEM_MAGIC_FACTOR, self.magic_factor)

        # GLOBAL MATERIAL PROPERTIES
        self.model_part.ProcessInfo.SetValue(NODAL_MASS_COEFF, self.nodal_mass_coeff)
     
        if (self.global_variables_option):
            self.model_part.ProcessInfo.SetValue(GLOBAL_KN, self.global_kn)
            self.model_part.ProcessInfo.SetValue(GLOBAL_KT, self.global_kt)

        # SEARCH-RELATED
        self.model_part.ProcessInfo.SetValue(SEARCH_RADIUS_EXTENSION, self.search_radius_extension)

        # PRINTING VARIABLES
        
        self.model_part.ProcessInfo.SetValue(FORCE_CALCULATION_TYPE, self.force_calculation_type_id)
        self.model_part.ProcessInfo.SetValue(DAMP_TYPE, self.damp_id)
        self.model_part.ProcessInfo.SetValue(ROTA_DAMP_TYPE, self.rota_damp_id)
        self.model_part.ProcessInfo.SetValue(INT_DUMMY_10, self.print_radial_displacement)#reserved for ON OFF print RADIAL_DISPLACEMENT
        self.model_part.ProcessInfo.SetValue(INT_DUMMY_8, self.print_group_id) # Reserved for: Export Print Group ID
        self.model_part.ProcessInfo.SetValue(INT_DUMMY_3, self.print_export_id) # Reserved for: Export Id

        # TIME RELATED PARAMETERS
        self.model_part.ProcessInfo.SetValue(DELTA_TIME, self.delta_time)
        self.model_part.ProcessInfo.SetValue(FINAL_SIMULATION_TIME, self.final_time)
        self.model_part.ProcessInfo.SetValue(INT_DUMMY_7, 0) # int(self.time_step_percentage_fix_velocities * (self.final_time / self.delta_time))) # Reserved for timestep fix_velocities

        # RESOLUTION METHODS AND PARAMETERS
        # Creating the solution strategy

        self.solver = ExplicitSolverStrategy(self.model_part, self.max_delta_time, self.n_step_search, self.safety_factor, self.move_mesh_flag, self.creator_destructor, self.time_scheme, self.search_strategy)

        self.solver.Initialize() # Calls the solver Initialized function (initializes all elements and performs other necessary tasks before iterating)

    #######################################################################

    def Solve(self):
        (self.solver).Solve()

    #######################################################################
