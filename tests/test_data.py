from process_navigator.extensions.database import db
from process_navigator.models.process import ProcessMethod
from process_navigator.models.units import BaseUnit, Unit, UnitCombination, UnitModifier
from process_navigator.models.analysis import AnalysisMethod, AnalysisMethodPart


def test_load_data(test_app):
    # check ProcessMethod and Process Method Parts

    with test_app.app_context():
        # check ProcessMethod and Process Method Parts
        query_process_methods_one = db.session.execute(db.select(ProcessMethod)).all()

        assert len(query_process_methods_one) == 1

        query_process_methods_two = db.session.execute(
            db.select(ProcessMethod).filter(
                ProcessMethod.name == "test_process_method_1"
            )
        ).scalar()

        assert query_process_methods_two is not None
        assert len(query_process_methods_two.process_method_parts) == 3

        # check Base Units
        query_base_units = db.session.scalars(db.select(BaseUnit)).all()

        assert len(query_base_units) == 3

        base_unit_names = [unit.name for unit in query_base_units]
        for unit in ["Meter", "Second", "Gram"]:
            assert unit in base_unit_names

        # check Unit Modifiers

        query_unit_modifiers = db.session.scalars(db.select(UnitModifier)).all()

        assert len(query_unit_modifiers) == 3

        unit_modifier_names = [unit.name for unit in query_unit_modifiers]
        for unit in ["Kilo", "Mega", "Milli"]:
            assert unit in unit_modifier_names

        # check units

        query_units = db.session.execute(db.select(Unit)).scalar_one()

        assert query_units.id == 1
        assert query_units.name == "Velocity"
        assert query_units.symbol == "Kms^-1"

        # check unit combinations

        query_unit_combinations = db.session.scalars(db.select(UnitCombination)).all()

        assert len(query_unit_combinations) == 2

        # check Anlaysis Method and Analysis Method Parts
        analysis_method_query = db.session.scalars(db.select(AnalysisMethod)).all()

        assert len(analysis_method_query) == 1
        assert analysis_method_query[0].name == "test_analysis_method_1"
        assert analysis_method_query[0].description == "test_description"

        # get part information
        part_name_list = [
            part.name for part in analysis_method_query[0].analysis_method_parts
        ]

        assert len(analysis_method_query[0].analysis_method_parts) == 3
        for part in ["test_part_1", "test_part_2", "test_part_3"]:
            assert part in part_name_list

        # check data type
        part = analysis_method_query[0].analysis_method_parts
        assert part[0].data_type == "Continuous"
        assert part[1].data_type == "Categorical"
        assert part[2].data_type == "String"

        # check only 3 AnalysisMethodParts were added:
        analysis_method_part_query = db.session.scalars(
            db.select(AnalysisMethodPart)
        ).all()
        assert len(analysis_method_part_query) == 3
