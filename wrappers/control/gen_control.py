# Copyright (C) 2007 Maryland Robotics Club
# Copyright (C) 2007 Joseph Lisee <jlisee@umd.edu>
# All rights reserved.
#
# Author: Joseph Lisee <jlisee@umd.edu>
# File:  wrappers/control/gen_control.py

import os

import buildfiles.wrap as wrap

def generate(module_builder, local_ns, global_ns):
    classes = []

    wrap.make_already_exposed(global_ns, 'ram::core', ['Subsystem'])
    wrap.make_already_exposed(global_ns, 'ram::math', ['Quaternion'],
                              no_implicit_conversion = True)

    # Include controller classes
    IController = local_ns.class_('IController')
    IController.include()
    
    IController.include_files.append(os.environ['RAM_SVN_DIR'] +
                                     '/packages/control/include/IController.h')

    # Wrap Events
    eventsFound = False
    for cls in local_ns.classes(function= lambda x: x.name.endswith('Event'),
                                allow_empty = True):
        cls.include()
        classes.append(cls)

    if eventsFound:
        wrap.make_already_exposed(global_ns, 'ram::core', ['Event'])

    # Add a castTo
    wrap.registerSubsystemConverter(IController)

    wrap.add_needed_includes(classes)
#    wrap.make_already_exposed(global_ns, 'ram::pattern', 'Subject')
    module_builder.add_registration_code("registerIControllerPtrs();")
    return ['wrappers/control/include/RegisterFunctions.h']

