//    |  /           |
//    ' /   __| _` | __|  _ \   __|
//    . \  |   (   | |   (   |\__ `
//   _|\_\_|  \__,_|\__|\___/ ____/
//                   Multi-Physics
//
//  License:		 BSD License
//					 Kratos default license: kratos/license.txt
//
//  Main authors:    Iñigo Lopez and Riccardo Rossi
//

#if !defined(KRATOS_COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION_VARIABLES_H_INCLUDED )
#define  KRATOS_COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION_VARIABLES_H_INCLUDED

// System includes

// External includes

// Project includes
#include "includes/define.h"
#include "includes/variables.h"
#include "includes/kratos_application.h"

namespace Kratos
{
// Degrees of freedom
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, double, POTENTIAL)
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, double, AUXILIARY_POTENTIAL)

// Flow field magnitudes
KRATOS_DEFINE_3D_APPLICATION_VARIABLE_WITH_COMPONENTS( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, VELOCITY_INFINITY)
KRATOS_DEFINE_3D_APPLICATION_VARIABLE_WITH_COMPONENTS( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, VELOCITY_LOWER)
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, double, PRESSURE_LOWER)
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, double, POTENTIAL_JUMP)
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, double, ENERGY_NORM_REFERENCE)
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, double, POTENTIAL_ENERGY_REFERENCE)

// Markers
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, bool, UPPER_SURFACE)
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, bool, LOWER_SURFACE)
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, bool, UPPER_WAKE)
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, bool, LOWER_WAKE)
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, int, AIRFOIL)
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, int, TRAILING_EDGE)
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, int, KUTTA)

// To be removed
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, int, TRAILING_EDGE_ELEMENT)
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, int, DECOUPLED_TRAILING_EDGE_ELEMENT)
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, int, DEACTIVATED_WAKE)
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, int, ALL_TRAILING_EDGE)
KRATOS_DEFINE_APPLICATION_VARIABLE( COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION, int, ZERO_VELOCITY_CONDITION)
}

#endif	/* KRATOS_COMPRESSIBLE_POTENTIAL_FLOW_APPLICATION_VARIABLES_H_INCLUDED */
