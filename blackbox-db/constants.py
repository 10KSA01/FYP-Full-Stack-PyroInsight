import sqlalchemy as sa
# Global variables for the blackbox-db project
error400 = 400
all300 = 300

column_na_defaults = {
    'reply_status':               'Failure',
    'flags':                      'None',
    'channel':                    'None',
    'channel_address':             error400,
    'point_category':             'None',
    'device_type':                'None',
    'raw_lta':                     error400,
    'dirtiness':                   error400,
    'loop_type':                  'None',
    'units_of_measure1':          'None',
    'units_of_measure2':          'None',
    'units_of_measure3':          'None',
    'converted_value1':            error400,
    'converted_value2':            error400,
    'converted_value3':            error400,
    'instantaneous_active_state': 'None',
    'instantaneous_fault_state' :  error400,
    'confirmed_active_state':      error400,
    'confirmed_fault_state':       error400,
    'acknowledged_active_state':   error400,
    'acknowledged_fault_state' :   error400,
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
    'dirtiness',
    'units_of_measure1',
    'units_of_measure2',
    'units_of_measure3',
    'converted_value1',
    'converted_value2',
    'converted_value3'
]

all_dtypes = {
    "id": str,
    "datetime": str,
    "reply_status": str,
    "flags": str,
    "node": str,
    "channel": str,
    "channel_address": str,
    "postr_category": str,
    "postr_number": str,
    "logical_postr_number": str,
    "logical_postr_zone": str,
    "device_type": str,
    "auxiliary_postr_attributes": str,
    "group": str,
    "area_type": str,
    "area_number": str,
    "sector_id": str,
    "loop_type": str,
    "raw_identity": str,
    "actual_device_type": str,
    "mode_and_sensitivity": str,
    "raw_analogue_values1": str,
    "raw_analogue_values2": str,
    "raw_analogue_values3": str,
    "lta_flags": str,
    "raw_lta": str,
    "dirtiness": str,
    "units_of_measure1": str,
    "units_of_measure2": str,
    "units_of_measure3": str,
    "converted_value1": str,
    "converted_value2": str,
    "converted_value3": str,
    "instantaneous_active_state": str,
    "instantaneous_fault_state": str,
    "confirmed_active_state": str,
    "confirmed_fault_state": str,
    "acknowledged_active_state": str,
    "acknowledged_fault_state": str,
    "output_forced_mode": str,
    "output_unforced_state": str,
    "output_forced_state": str
}
# Define the column data types
dtypes = {
    'id':                   sa.String(length=30),
    'datetime':             sa.TIMESTAMP(),
    'reply_status':         sa.String(length=10),
    'node':                 sa.Integer(),
    'channel_address':      sa.Integer(),
    'point_number':         sa.String(length=50),
    'logical_point_number': sa.Integer(),
    'logical_point_zone':   sa.String(length=20),
    'device_type':          sa.String(length=50),
    'dirtiness':            sa.Integer(),
    'units_of_measure1':    sa.String(length=30), 
    'units_of_measure2':    sa.String(length=30),
    'units_of_measure3':    sa.String(length=30),
    'converted_value1':     sa.Integer(),
    'converted_value2':     sa.Integer(),
    'converted_value3':     sa.Integer()
}

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


