from scripts.predict import model


def test_model_existence():
    assert model.get_params() is not None
