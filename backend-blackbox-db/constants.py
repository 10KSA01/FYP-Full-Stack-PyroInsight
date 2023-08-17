# Global variables for the blackbox-db project
error400 = 400
all300 = 300

column_na_defaults = {
    'reply_status':               'Failure',
    'flags':                      'None',
    'channel':                    'None',
    'channel_address':             400,
    'point_category':             'None',
    'device_type':                'None',
    'dirtiness':                   400,
    'loop_type':                  'None',
    'units_of_measure1':          'None',
    'units_of_measure2':          'None',
    'units_of_measure3':          'None',
    'instantaneous_active_state': 'None',
    'output_forced_mode':         'None',
    'output_unforced_state':      'None',
    'output_forced_state':        'None'
}

format_datetime = "%Y-%m-%d %H:%M:%S"

columns_to_upload = [
    'id', 
    'datetime', 
    'reply_status', 
    'node', 
    'channel_address', 
    'point_number', 
    'logical_point_number', 
    'logical_point_zone', 
    'device_type', 
    'dirtiness'
    ]

float_to_int64 = [
    'node', 
    'channel_address', 
    'logical_point_number', 
    'auxiliary_point_attributes', 
    'group', 
    'area_type', 
    'area_number', 
    'raw_identity', 
    'actual_device_type', 
    'mode_and_sensitivity', 
    'raw_analogue_values1', 
    'raw_analogue_values2', 
    'raw_analogue_values3',
    'raw_lta', 
    'dirtiness', 
    'converted_value1', 
    'converted_value2', 
    'converted_value3',
    'instantaneous_fault_state',
    'confirmed_fault_state', 
    'acknowledged_active_state', 
    'acknowledged_fault_state'
    ]
        
unique_id = [
    'node', 
    'channel_address', 
    'point_number', 
    'logical_point_number', 
    'logical_point_zone'
    ]
        
