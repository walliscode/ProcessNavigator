"""
Data generators for creating large or complex test datasets.

These generators create realistic test data for various scenarios including
performance testing, edge cases, and complex workflows.
"""

import random
import string
from typing import List, Dict, Any


def generate_process_methods(count: int, with_parts: bool = True, parts_per_method: int = 3) -> List[Dict[str, Any]]:
    """
    Generate process method data for testing.
    
    Args:
        count: Number of process methods to generate
        with_parts: Whether to include process method parts
        parts_per_method: Number of parts per method
    
    Returns:
        List of process method data dictionaries
    """
    methods = []
    
    for i in range(count):
        method = {
            "name": f"Process Method {i+1}",
            "description": f"Description for process method {i+1}",
            "file_name": f"process_{i+1}.txt",
        }
        
        if with_parts:
            method["parts"] = [
                {"name": f"Part {j+1}"} 
                for j in range(parts_per_method)
            ]
        
        methods.append(method)
    
    return methods


def generate_inputs(count: int, unit_ids: List[int] = None) -> List[Dict[str, Any]]:
    """
    Generate input material data for testing.
    
    Args:
        count: Number of inputs to generate
        unit_ids: List of unit IDs to randomly assign (optional)
    
    Returns:
        List of input data dictionaries
    """
    if unit_ids is None:
        unit_ids = [1]  # Default unit ID
    
    inputs = []
    
    # Common chemical names for realistic testing
    chemical_prefixes = ["Methyl", "Ethyl", "Propyl", "Butyl", "Phenyl"]
    chemical_suffixes = ["amine", "alcohol", "acid", "ester", "oxide"]
    
    for i in range(count):
        prefix = random.choice(chemical_prefixes)
        suffix = random.choice(chemical_suffixes)
        
        # Generate realistic CAS number format
        cas_parts = [
            random.randint(10, 9999),
            random.randint(10, 99),
            random.randint(0, 9)
        ]
        cas = f"{cas_parts[0]}-{cas_parts[1]}-{cas_parts[2]}"
        
        inputs.append({
            "name": f"{prefix} {suffix} {i+1}",
            "CAS": cas,
            "unit_id": random.choice(unit_ids)
        })
    
    return inputs


def generate_parameters(count: int, unit_ids: List[int] = None) -> List[Dict[str, Any]]:
    """
    Generate parameter data for testing.
    
    Args:
        count: Number of parameters to generate
        unit_ids: List of unit IDs to randomly assign (optional)
    
    Returns:
        List of parameter data dictionaries
    """
    if unit_ids is None:
        unit_ids = [1]
    
    # Common parameter names
    param_types = [
        "Temperature", "Pressure", "Flow Rate", "Concentration",
        "Time", "Volume", "Mass", "pH", "Speed", "Power"
    ]
    
    parameters = []
    
    for i in range(count):
        param_type = random.choice(param_types)
        stage = random.randint(1, 10)
        
        parameters.append({
            "name": f"{param_type} Stage {stage}",
            "unit_id": random.choice(unit_ids)
        })
    
    return parameters


def generate_analysis_methods(count: int, with_parts: bool = True, parts_per_method: int = 5) -> List[Dict[str, Any]]:
    """
    Generate analysis method data for testing.
    
    Args:
        count: Number of analysis methods to generate
        with_parts: Whether to include analysis method parts
        parts_per_method: Number of parts per method
    
    Returns:
        List of analysis method data dictionaries
    """
    analysis_types = [
        "HPLC", "GC-MS", "NMR", "IR Spectroscopy", "Mass Spectrometry",
        "Chromatography", "Titration", "Microscopy"
    ]
    
    methods = []
    
    for i in range(count):
        analysis_type = random.choice(analysis_types)
        
        method = {
            "name": f"{analysis_type} Method {i+1}",
            "description": f"Analysis using {analysis_type}",
            "file_name": f"analysis_{i+1}.txt",
        }
        
        if with_parts:
            data_types = ["float", "int", "string"]
            method["parts"] = [
                {
                    "name": f"Measurement {j+1}",
                    "unit_id": 1,  # Default unit
                    "data_type": random.choice(data_types)
                }
                for j in range(parts_per_method)
            ]
        
        methods.append(method)
    
    return methods


def generate_user_paths(complexity: str = "simple") -> List[Dict[str, Any]]:
    """
    Generate user path scenarios for testing.
    
    Args:
        complexity: Complexity level - "simple", "medium", or "complex"
    
    Returns:
        List of user path dictionaries
    """
    paths = []
    
    if complexity == "simple":
        paths.append({
            "name": "simple_login",
            "description": "User registers and logs in",
            "path": ["register_user", "login_user"]
        })
        
    elif complexity == "medium":
        paths.append({
            "name": "create_process_method",
            "description": "User creates a process method",
            "path": [
                "register_user",
                "login_user",
                "data_index_get",
                "process_method_get",
                "process_method_post_add_method",
                "add_process_method_get"
            ]
        })
        
    elif complexity == "complex":
        paths.append({
            "name": "full_workflow",
            "description": "User completes full process path creation",
            "path": [
                "register_user",
                "login_user",
                "data_index_get",
                "process_method_get",
                "process_method_post_add_method",
                "add_process_method_get",
                "inputs_get",
                "inputs_post_add_input",
                "add_input_get",
                "cauldron_index_get",
                "cauldron_index_post_start",
                "cauldron_process_path_get"
            ]
        })
    
    return paths


def generate_large_dataset(tables: Dict[str, int]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Generate large dataset for performance testing.
    
    Args:
        tables: Dictionary mapping table names to record counts
                e.g., {"ProcessMethods": 100, "Inputs": 1000}
    
    Returns:
        Dictionary with generated data for each table
    """
    dataset = {}
    
    for table, count in tables.items():
        if table == "ProcessMethods":
            dataset[table] = generate_process_methods(count)
        elif table == "Inputs":
            dataset[table] = generate_inputs(count)
        elif table == "Parameters":
            dataset[table] = generate_parameters(count)
        elif table == "AnalysisMethods":
            dataset[table] = generate_analysis_methods(count)
    
    return dataset


def generate_edge_case_data() -> Dict[str, List[Dict[str, Any]]]:
    """
    Generate edge case data for boundary testing.
    
    Returns:
        Dictionary with edge case test data
    """
    return {
        "empty_strings": [
            {"name": "", "description": "Empty name"},
            {"name": "Valid", "description": ""},
        ],
        "long_strings": [
            {"name": "A" * 255, "description": "Maximum length name"},
            {"name": "Short", "description": "B" * 1000},
        ],
        "special_characters": [
            {"name": "Test<script>alert('xss')</script>", "description": "XSS attempt"},
            {"name": "Test'; DROP TABLE users; --", "description": "SQL injection attempt"},
            {"name": "Test\n\r\t", "description": "Whitespace characters"},
        ],
        "unicode": [
            {"name": "Test 测试", "description": "Chinese characters"},
            {"name": "Test مرحبا", "description": "Arabic characters"},
            {"name": "Test 🔬", "description": "Emoji"},
        ],
        "null_values": [
            {"name": None, "description": "Null name"},
            {"name": "Valid", "description": None},
        ],
        "numeric_boundaries": [
            {"multiplier": 0},
            {"multiplier": 0.000001},
            {"multiplier": 999999999},
            {"multiplier": -1},
        ],
    }


def generate_realistic_cas_numbers(count: int) -> List[str]:
    """
    Generate realistic CAS registry numbers.
    
    Args:
        count: Number of CAS numbers to generate
    
    Returns:
        List of CAS number strings
    """
    cas_numbers = []
    
    for _ in range(count):
        # CAS format: 2-7 digits, hyphen, 2 digits, hyphen, 1 digit check
        part1 = random.randint(10, 9999999)
        part2 = random.randint(10, 99)
        part3 = random.randint(0, 9)
        
        cas_numbers.append(f"{part1}-{part2}-{part3}")
    
    return cas_numbers


def generate_unit_combinations(base_units: List[Dict], modifiers: List[Dict], count: int) -> List[Dict[str, Any]]:
    """
    Generate unit combination data.
    
    Args:
        base_units: List of base unit dictionaries
        modifiers: List of modifier dictionaries
        count: Number of combinations to generate
    
    Returns:
        List of unit combination dictionaries
    """
    combinations = []
    
    for i in range(count):
        base_unit = random.choice(base_units)
        modifier = random.choice(modifiers)
        power = random.choice([-2, -1, 1, 2, 3])
        
        combinations.append({
            "unit_id": 1,  # Parent unit ID
            "base_unit_id": base_unit.get("id", i),
            "unit_modifier_id": modifier.get("id", i),
            "power": power
        })
    
    return combinations


def generate_test_scenario(scenario_type: str) -> Dict[str, Any]:
    """
    Generate complete test scenario with all necessary data.
    
    Args:
        scenario_type: Type of scenario - "minimal", "standard", or "large"
    
    Returns:
        Dictionary with complete scenario data
    """
    scenarios = {
        "minimal": {
            "ProcessMethods": generate_process_methods(1, parts_per_method=2),
            "BaseUnits": [
                {"name": "Meter", "symbol": "m"},
                {"name": "Second", "symbol": "s"}
            ],
            "UnitModifiers": [
                {"name": "Kilo", "symbol": "K", "multiplier": 1000}
            ],
            "Inputs": generate_inputs(2),
            "Parameters": generate_parameters(2),
        },
        "standard": {
            "ProcessMethods": generate_process_methods(3, parts_per_method=3),
            "BaseUnits": [
                {"name": "Meter", "symbol": "m"},
                {"name": "Second", "symbol": "s"},
                {"name": "Gram", "symbol": "g"},
                {"name": "Kelvin", "symbol": "K"}
            ],
            "UnitModifiers": [
                {"name": "Kilo", "symbol": "K", "multiplier": 1000},
                {"name": "Milli", "symbol": "m", "multiplier": 0.001}
            ],
            "Inputs": generate_inputs(10),
            "Parameters": generate_parameters(10),
            "AnalysisMethods": generate_analysis_methods(2),
        },
        "large": {
            "ProcessMethods": generate_process_methods(50, parts_per_method=5),
            "BaseUnits": [
                {"name": "Meter", "symbol": "m"},
                {"name": "Second", "symbol": "s"},
                {"name": "Gram", "symbol": "g"},
                {"name": "Kelvin", "symbol": "K"},
                {"name": "Mole", "symbol": "mol"}
            ],
            "UnitModifiers": [
                {"name": "Kilo", "symbol": "K", "multiplier": 1000},
                {"name": "Mega", "symbol": "M", "multiplier": 1000000},
                {"name": "Milli", "symbol": "m", "multiplier": 0.001},
                {"name": "Micro", "symbol": "μ", "multiplier": 0.000001}
            ],
            "Inputs": generate_inputs(100),
            "Parameters": generate_parameters(100),
            "AnalysisMethods": generate_analysis_methods(20),
        }
    }
    
    return scenarios.get(scenario_type, scenarios["standard"])


def generate_random_workflow_data() -> Dict[str, Any]:
    """
    Generate random but valid workflow data for testing.
    
    Returns:
        Dictionary with workflow data
    """
    return {
        "user": {
            "email": f"user_{random.randint(1000, 9999)}@test.com",
            "password": "".join(random.choices(string.ascii_letters + string.digits, k=12)),
            "first_name": random.choice(["John", "Jane", "Alex", "Sam"]),
            "last_name": random.choice(["Smith", "Johnson", "Williams", "Brown"])
        },
        "process_method": {
            "name": f"Process {random.randint(1, 1000)}",
            "description": "Auto-generated process method",
            "file_name": f"process_{random.randint(1, 1000)}.txt"
        },
        "inputs": [
            {
                "name": f"Input {i}",
                "CAS": f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(0, 9)}",
                "unit_id": 1
            }
            for i in range(random.randint(2, 5))
        ],
        "parameters": [
            {
                "name": f"Parameter {i}",
                "unit_id": 1
            }
            for i in range(random.randint(2, 5))
        ]
    }
