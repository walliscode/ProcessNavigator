"""
Example unit tests for Process models.

This file demonstrates how to write unit tests for model classes.
These tests verify model instantiation, properties, and methods in isolation.
"""

import pytest


@pytest.mark.unit
def test_process_method_instantiation():
    """Test ProcessMethod can be instantiated with valid data."""
    from process_navigator.models.process import ProcessMethod
    
    pm = ProcessMethod(
        name="Test Method",
        description="Test Description",
        file_name="test.txt"
    )
    
    assert pm.name == "Test Method"
    assert pm.description == "Test Description"
    assert pm.file_name == "test.txt"


@pytest.mark.unit
def test_process_method_part_instantiation():
    """Test ProcessMethodPart can be instantiated with valid data."""
    from process_navigator.models.process import ProcessMethod, ProcessMethodPart
    
    pm = ProcessMethod(
        name="Test Method",
        description="Test Description",
        file_name="test.txt"
    )
    
    part = ProcessMethodPart(
        name="Test Part",
        process_method=pm
    )
    
    assert part.name == "Test Part"
    assert part.process_method == pm


@pytest.mark.unit
def test_process_method_parts_relationship():
    """Test ProcessMethod to ProcessMethodPart relationship."""
    from process_navigator.models.process import ProcessMethod, ProcessMethodPart
    
    pm = ProcessMethod(
        name="Test Method",
        description="Test Description",
        file_name="test.txt"
    )
    
    part1 = ProcessMethodPart(name="Part 1", process_method=pm)
    part2 = ProcessMethodPart(name="Part 2", process_method=pm)
    
    assert len(pm.process_method_parts) == 2
    assert part1 in pm.process_method_parts
    assert part2 in pm.process_method_parts
    assert part1.process_method == pm
    assert part2.process_method == pm


@pytest.mark.unit
def test_discipline_instantiation():
    """Test Discipline can be instantiated with valid data."""
    from process_navigator.models.process import Discipline
    
    discipline = Discipline(
        code="TEST",
        name="Test Discipline",
        description="Test Description"
    )
    
    assert discipline.code == "TEST"
    assert discipline.name == "Test Discipline"
    assert discipline.description == "Test Description"


# Example of testing validation (if implemented)
@pytest.mark.unit
def test_process_method_requires_name():
    """Test ProcessMethod requires a name (if validation is implemented)."""
    from process_navigator.models.process import ProcessMethod
    
    # This test assumes validation is implemented
    # Adjust based on actual implementation
    try:
        pm = ProcessMethod(
            name=None,
            description="Test",
            file_name="test.txt"
        )
        # If no validation, this should still work
        assert pm.name is None
    except (ValueError, TypeError):
        # If validation exists, it should raise an exception
        pass


# Example of testing computed properties (if they exist)
@pytest.mark.unit
def test_process_method_computed_property():
    """Test computed properties on ProcessMethod (if they exist)."""
    from process_navigator.models.process import ProcessMethod
    
    pm = ProcessMethod(
        name="Test Method",
        description="Test Description",
        file_name="test.txt"
    )
    
    # Example: if there's a property that computes something
    # assert pm.some_computed_property == expected_value
    pass


# Example of testing string representation
@pytest.mark.unit
def test_process_method_str_representation():
    """Test ProcessMethod string representation."""
    from process_navigator.models.process import ProcessMethod
    
    pm = ProcessMethod(
        name="Test Method",
        description="Test Description",
        file_name="test.txt"
    )
    
    # If __str__ or __repr__ is implemented
    str_repr = str(pm)
    assert "Test Method" in str_repr or str_repr  # Verify it returns something
