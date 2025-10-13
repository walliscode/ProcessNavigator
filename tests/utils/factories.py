"""
Test data factories for creating model instances.

Factories provide a convenient way to create test data with sensible defaults
while allowing customization of specific attributes.
"""

from typing import Optional, Dict, Any


class BaseFactory:
    """Base factory class with common functionality."""
    
    @staticmethod
    def _generate_unique_name(prefix="test"):
        """Generate a unique name with timestamp."""
        import time
        return f"{prefix}_{int(time.time() * 1000000)}"


class ProcessMethodFactory(BaseFactory):
    """Factory for creating ProcessMethod instances."""
    
    @staticmethod
    def build(**kwargs) -> Dict[str, Any]:
        """
        Build ProcessMethod data dictionary (not persisted).
        
        Args:
            **kwargs: Override default values
        
        Returns:
            Dictionary with ProcessMethod attributes
        """
        defaults = {
            "name": ProcessMethodFactory._generate_unique_name("process_method"),
            "description": "Test process method description",
            "file_name": "test_process.txt",
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create(db_session, **kwargs):
        """
        Create and persist ProcessMethod instance.
        
        Args:
            db_session: Database session
            **kwargs: Override default values
        
        Returns:
            ProcessMethod instance
        """
        from process_navigator.models.process import ProcessMethod
        
        data = ProcessMethodFactory.build(**kwargs)
        instance = ProcessMethod(**data)
        db_session.add(instance)
        db_session.commit()
        return instance
    
    @staticmethod
    def create_batch(db_session, count, **kwargs):
        """
        Create multiple ProcessMethod instances.
        
        Args:
            db_session: Database session
            count: Number of instances to create
            **kwargs: Override default values
        
        Returns:
            List of ProcessMethod instances
        """
        instances = []
        for i in range(count):
            data = kwargs.copy()
            if "name" not in data:
                data["name"] = f"process_method_{i}_{ProcessMethodFactory._generate_unique_name()}"
            instances.append(ProcessMethodFactory.create(db_session, **data))
        return instances


class ProcessMethodPartFactory(BaseFactory):
    """Factory for creating ProcessMethodPart instances."""
    
    @staticmethod
    def build(process_method_id=None, **kwargs) -> Dict[str, Any]:
        """Build ProcessMethodPart data dictionary."""
        defaults = {
            "name": ProcessMethodPartFactory._generate_unique_name("part"),
            "process_method_id": process_method_id,
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create(db_session, process_method=None, **kwargs):
        """
        Create and persist ProcessMethodPart instance.
        
        Args:
            db_session: Database session
            process_method: ProcessMethod instance (optional)
            **kwargs: Override default values
        
        Returns:
            ProcessMethodPart instance
        """
        from process_navigator.models.process import ProcessMethodPart
        
        if process_method:
            kwargs["process_method_id"] = process_method.id
            kwargs["process_method"] = process_method
        
        data = ProcessMethodPartFactory.build(**kwargs)
        instance = ProcessMethodPart(**data)
        db_session.add(instance)
        db_session.commit()
        return instance


class UserFactory(BaseFactory):
    """Factory for creating User instances."""
    
    @staticmethod
    def build(**kwargs) -> Dict[str, Any]:
        """Build User data dictionary."""
        defaults = {
            "first_name": "Test",
            "last_name": "User",
            "email": f"test_{UserFactory._generate_unique_name()}@example.com",
            "password": "testpassword123",
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create(db_session, **kwargs):
        """
        Create and persist User instance.
        
        Args:
            db_session: Database session
            **kwargs: Override default values
        
        Returns:
            User instance
        """
        from process_navigator.models import User
        
        data = UserFactory.build(**kwargs)
        instance = User(**data)
        db_session.add(instance)
        db_session.commit()
        return instance


class BaseUnitFactory(BaseFactory):
    """Factory for creating BaseUnit instances."""
    
    @staticmethod
    def build(**kwargs) -> Dict[str, Any]:
        """Build BaseUnit data dictionary."""
        defaults = {
            "name": BaseUnitFactory._generate_unique_name("unit"),
            "symbol": "u",
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create(db_session, **kwargs):
        """Create and persist BaseUnit instance."""
        from process_navigator.models.units import BaseUnit
        
        data = BaseUnitFactory.build(**kwargs)
        instance = BaseUnit(**data)
        db_session.add(instance)
        db_session.commit()
        return instance
    
    @staticmethod
    def create_common_units(db_session):
        """Create common base units (meter, second, gram, etc.)."""
        common_units = [
            {"name": "Meter", "symbol": "m"},
            {"name": "Second", "symbol": "s"},
            {"name": "Gram", "symbol": "g"},
            {"name": "Kelvin", "symbol": "K"},
            {"name": "Mole", "symbol": "mol"},
        ]
        return [BaseUnitFactory.create(db_session, **unit) for unit in common_units]


class UnitModifierFactory(BaseFactory):
    """Factory for creating UnitModifier instances."""
    
    @staticmethod
    def build(**kwargs) -> Dict[str, Any]:
        """Build UnitModifier data dictionary."""
        defaults = {
            "name": UnitModifierFactory._generate_unique_name("modifier"),
            "symbol": "x",
            "multiplier": 1.0,
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create(db_session, **kwargs):
        """Create and persist UnitModifier instance."""
        from process_navigator.models.units import UnitModifier
        
        data = UnitModifierFactory.build(**kwargs)
        instance = UnitModifier(**data)
        db_session.add(instance)
        db_session.commit()
        return instance
    
    @staticmethod
    def create_common_modifiers(db_session):
        """Create common unit modifiers (kilo, mega, milli, etc.)."""
        common_modifiers = [
            {"name": "Kilo", "symbol": "K", "multiplier": 1000},
            {"name": "Mega", "symbol": "M", "multiplier": 1000000},
            {"name": "Milli", "symbol": "m", "multiplier": 0.001},
            {"name": "Micro", "symbol": "μ", "multiplier": 0.000001},
        ]
        return [UnitModifierFactory.create(db_session, **mod) for mod in common_modifiers]


class UnitFactory(BaseFactory):
    """Factory for creating Unit instances."""
    
    @staticmethod
    def build(**kwargs) -> Dict[str, Any]:
        """Build Unit data dictionary."""
        defaults = {
            "name": UnitFactory._generate_unique_name("unit"),
            "symbol": "U",
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create(db_session, **kwargs):
        """Create and persist Unit instance."""
        from process_navigator.models.units import Unit
        
        data = UnitFactory.build(**kwargs)
        instance = Unit(**data)
        db_session.add(instance)
        db_session.commit()
        return instance


class InputFactory(BaseFactory):
    """Factory for creating Input instances."""
    
    @staticmethod
    def build(unit_id=None, **kwargs) -> Dict[str, Any]:
        """Build Input data dictionary."""
        defaults = {
            "name": InputFactory._generate_unique_name("input"),
            "CAS": "123-45-6",
            "unit_id": unit_id,
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create(db_session, unit=None, **kwargs):
        """
        Create and persist Input instance.
        
        Args:
            db_session: Database session
            unit: Unit instance (optional)
            **kwargs: Override default values
        
        Returns:
            Input instance
        """
        from process_navigator.models.inputs import Input
        
        if unit:
            kwargs["unit_id"] = unit.id
            kwargs["unit"] = unit
        
        data = InputFactory.build(**kwargs)
        instance = Input(**data)
        db_session.add(instance)
        db_session.commit()
        return instance


class ParamFactory(BaseFactory):
    """Factory for creating Param instances."""
    
    @staticmethod
    def build(unit_id=None, **kwargs) -> Dict[str, Any]:
        """Build Param data dictionary."""
        defaults = {
            "name": ParamFactory._generate_unique_name("param"),
            "unit_id": unit_id,
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create(db_session, unit=None, **kwargs):
        """Create and persist Param instance."""
        from process_navigator.models.parameters import Param
        
        if unit:
            kwargs["unit_id"] = unit.id
            kwargs["unit"] = unit
        
        data = ParamFactory.build(**kwargs)
        instance = Param(**data)
        db_session.add(instance)
        db_session.commit()
        return instance


class AnalysisMethodFactory(BaseFactory):
    """Factory for creating AnalysisMethod instances."""
    
    @staticmethod
    def build(**kwargs) -> Dict[str, Any]:
        """Build AnalysisMethod data dictionary."""
        defaults = {
            "name": AnalysisMethodFactory._generate_unique_name("analysis"),
            "description": "Test analysis method description",
            "file_name": "test_analysis.txt",
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create(db_session, **kwargs):
        """Create and persist AnalysisMethod instance."""
        from process_navigator.models.analysis import AnalysisMethod
        
        data = AnalysisMethodFactory.build(**kwargs)
        instance = AnalysisMethod(**data)
        db_session.add(instance)
        db_session.commit()
        return instance


class AnalysisMethodPartFactory(BaseFactory):
    """Factory for creating AnalysisMethodPart instances."""
    
    @staticmethod
    def build(analysis_method_id=None, unit_id=None, **kwargs) -> Dict[str, Any]:
        """Build AnalysisMethodPart data dictionary."""
        defaults = {
            "name": AnalysisMethodPartFactory._generate_unique_name("analysis_part"),
            "analysis_method_id": analysis_method_id,
            "unit_id": unit_id,
            "data_type": "float",
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create(db_session, analysis_method=None, unit=None, **kwargs):
        """Create and persist AnalysisMethodPart instance."""
        from process_navigator.models.analysis import AnalysisMethodPart
        
        if analysis_method:
            kwargs["analysis_method_id"] = analysis_method.id
            kwargs["analysis_method"] = analysis_method
        
        if unit:
            kwargs["unit_id"] = unit.id
        
        data = AnalysisMethodPartFactory.build(**kwargs)
        instance = AnalysisMethodPart(**data)
        db_session.add(instance)
        db_session.commit()
        return instance


class DisciplineFactory(BaseFactory):
    """Factory for creating Discipline instances."""
    
    @staticmethod
    def build(**kwargs) -> Dict[str, Any]:
        """Build Discipline data dictionary."""
        defaults = {
            "code": DisciplineFactory._generate_unique_name("DISC"),
            "name": "Test Discipline",
            "description": "Test discipline description",
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create(db_session, **kwargs):
        """Create and persist Discipline instance."""
        from process_navigator.models.process import Discipline
        
        data = DisciplineFactory.build(**kwargs)
        instance = Discipline(**data)
        db_session.add(instance)
        db_session.commit()
        return instance


# Convenience function for creating complete test scenarios
def create_complete_test_scenario(db_session):
    """
    Create a complete test scenario with all related entities.
    
    Returns:
        Dictionary with all created entities
    """
    # Create base units and modifiers
    base_units = BaseUnitFactory.create_common_units(db_session)
    modifiers = UnitModifierFactory.create_common_modifiers(db_session)
    
    # Create a composite unit
    unit = UnitFactory.create(db_session, name="Velocity", symbol="m/s")
    
    # Create inputs and parameters
    input1 = InputFactory.create(db_session, unit=unit, name="Water", CAS="7732-18-5")
    param1 = ParamFactory.create(db_session, unit=unit, name="Flow Rate")
    
    # Create process method with parts
    process_method = ProcessMethodFactory.create(db_session)
    part1 = ProcessMethodPartFactory.create(db_session, process_method=process_method)
    part2 = ProcessMethodPartFactory.create(db_session, process_method=process_method)
    
    # Create analysis method with parts
    analysis_method = AnalysisMethodFactory.create(db_session)
    analysis_part = AnalysisMethodPartFactory.create(
        db_session, 
        analysis_method=analysis_method,
        unit=unit
    )
    
    # Create discipline
    discipline = DisciplineFactory.create(db_session)
    
    # Create user
    user = UserFactory.create(db_session)
    
    return {
        "base_units": base_units,
        "modifiers": modifiers,
        "unit": unit,
        "input": input1,
        "param": param1,
        "process_method": process_method,
        "process_method_parts": [part1, part2],
        "analysis_method": analysis_method,
        "analysis_method_part": analysis_part,
        "discipline": discipline,
        "user": user,
    }
