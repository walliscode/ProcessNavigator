from process_navigator.extensions import db
from process_navigator.models.process import ProcessMethod, ProcessMethodPart


def load_test_data(json_data):
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
