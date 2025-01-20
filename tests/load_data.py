from process_navigator.models.parameters import Param
from process_navigator.models.process import ProcessMethod, ProcessMethodPart
from process_navigator.models.units import BaseUnit, Unit, UnitCombination, UnitModifier
from process_navigator.models.analysis import AnalysisMethod, AnalysisMethodPart


def load_test_data(json_data, db):
    # load process methods
    for method in json_data["ProcessMethods"]:
        new_method = ProcessMethod(
            name=method["name"],
            description=method["description"],
            file_name=method["file_name"],
        )
        db.session.add(new_method)
        db.session.commit()
        for part in method["parts"]:
            new_part = ProcessMethodPart(
                name=part["name"],
                process_method_id=new_method.id,
                process_method=new_method,
            )
            db.session.add(new_part)

        db.session.commit()

    # load Base Units
    for unit in json_data["BaseUnits"]:
        new_unit = BaseUnit(
            name=unit["name"],
            symbol=unit["symbol"],
        )
        db.session.add(new_unit)
        db.session.commit()

    # load Unit Modifiers

    for unit in json_data["UnitModifiers"]:
        new_unit_modifier = UnitModifier(
            name=unit["name"],
            symbol=unit["symbol"],
            multiplier=unit["multiplier"],
        )
        db.session.add(new_unit_modifier)
        db.session.commit()

    # load Units

    for unit in json_data["Units"]:
        # first create combined symbol

        new_unit = Unit(
            name=unit["name"],
        )
        db.session.add(new_unit)
        db.session.commit()

        for combo in unit["UnitCombinations"]:
            # get the base unit
            base_unit = db.session.execute(
                db.select(BaseUnit).filter(BaseUnit.name == combo["base_unit"])
            ).scalar()

            # get the unit modifier
            modifier = db.session.execute(
                db.select(UnitModifier).filter(UnitModifier.name == combo["modifier"])
            ).scalar()

            new_combo = UnitCombination(
                unit_id=new_unit.id,
                unit=new_unit,
                base_unit_id=base_unit.id,
                base_unit=base_unit,
                unit_modifier_id=modifier.id if modifier is not None else None,
                unit_modifier=modifier if modifier is not None else None,
                exponent=combo["exponent"],
            )

            db.session.add(new_combo)

        db.session.commit()

    for method in json_data["AnalysisMethods"]:
        new_method = AnalysisMethod(
            name=method["name"],
            description=method["description"],
            file_name=method["file_name"],
        )

        db.session.add(new_method)
        db.session.commit()

        for part in method["parts"]:
            new_part = AnalysisMethodPart(
                name=part["name"],
                unit_id=part["unit_id"],
                analysis_method_id=new_method.id,
                analysis_method=new_method,
                data_type=part["data_type"],
            )

            db.session.add(new_part)
            db.session.commit()

    for parameter in json_data["Parameters"]:
        # get unit object
        unit_get = db.session.execute(
            db.select(Unit).filter(Unit.id == parameter["unit_id"])
        ).scalar()
        new_parameter = Param(
            name=parameter["name"],
            unit_id=parameter["unit_id"],
            unit=unit_get,
        )

        db.session.add(new_parameter)
        db.session.commit()
