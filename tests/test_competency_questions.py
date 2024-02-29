from glob import glob
import subprocess as sp
from pathlib import Path
import os
import shutil

CWD = os.getcwd()
with open(Path(CWD).joinpath("VERSION").as_posix()) as version_file:
    __version__ = version_file.readlines()[0].strip()

ROBOT_JAR = Path(CWD).joinpath("robot.jar").as_posix()
JAVA_PATH = Path(shutil.which("java"))
CATALOG_PATH = Path(CWD).joinpath("src/catalog-v001.xml")
ONTOLOGY_PATH = Path(CWD).joinpath("src").joinpath("chio.ttl").as_posix()
COMPETENCY_QUESTION_DIRECTORY = Path(CWD).joinpath("tests/cqs")


def pytest_generate_tests(metafunc):
    if "competency_question_path" in metafunc.fixturenames:
        competency_question_list = [
            p
            for p in glob(
                COMPETENCY_QUESTION_DIRECTORY.as_posix() + "/**/*.rq", recursive=True
            )
        ]
        metafunc.parametrize("competency_question_path", competency_question_list)


def check_competency_question(query, ontology, tmp):
    """Check competency question against the given ontology

    Args:
        conclusion (str): A filepath to the competency question.
        premise (str): A filepath to the reference ontology.

    Raises:
        RuntimeError: If calling ROBOT raises an error this will be raised as a RuntimeError.

    Returns:
        (boolean): Returns True if the competency question was sucessfully checked against the ontology.
    """
    query_call = (
        f"java -jar {ROBOT_JAR} merge --input {ontology} --catalog {CATALOG_PATH.as_posix()} "
        + f"query --format ttl --query {query} {tmp}"
    )
    response = sp.call(query_call)
    if response != 0:
        raise RuntimeError(f"Response: {response}")
    with open(f"{tmp}", "r") as f:
        result = {"true": True, "false": False}.get(f.readline(), None)
        if result is None:
            raise RuntimeError("The query did not return a boolean.")

    assert result, f"Question {query} was not satisfied."


def test_competency_question(
    competency_question_path,
    tmp_path_factory,
):
    """Metatest to produce competency question tests."""
    tmppath = tmp_path_factory.mktemp("data") / "test.ttl"
    check_competency_question(competency_question_path, ONTOLOGY_PATH, tmppath)
