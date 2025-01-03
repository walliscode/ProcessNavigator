from process_navigator.extensions import db
from process_navigator.models.process import ProcessMethod


def test_load_data(test_app):
    # check ProcessMethod and Process Method Parts

    with test_app.app_context():
        query_process_methods_one = db.session.execute(db.select(ProcessMethod)).all()

        assert len(query_process_methods_one) == 1

        query_process_methods_two = db.session.execute(
            db.select(ProcessMethod).filter(
                ProcessMethod.name == "test_process_method_1"
            )
        ).scalar()

        assert query_process_methods_two is not None
        assert len(query_process_methods_two.process_method_parts) == 3
