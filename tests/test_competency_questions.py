from glob import glob
import subprocess as sp
from pathlib import Path
import os
import shutil

CWD = os.getcwd()
with open(Path(CWD).joinpath("VERSION").as_posix()) as version_file:
    __version__ = version_file.readlines()[0].strip()

ROBOT_JAR = Path(CWD).joinpath("robot.jar").as_posix()
HERMIT_JAR = Path(CWD).joinpath("hermit.jar").as_posix()
CATALOG_PATH = Path(CWD).joinpath("src/catalog-v001.xml")
ONTOLOGY_PATH = Path(CWD).joinpath("src").joinpath("chio.ttl").as_posix()
CQ_ABOX = Path(CWD).joinpath("tests/cq_abox")
CQ_TBOX = Path(CWD).joinpath("tests/cq_tbox")
INSTANCE_PATH = Path(CWD).joinpath("tests/cq_instances")
JAVA_PATH = shutil.which("java")


def pytest_generate_tests(metafunc):
    if "cq_abox_path" in metafunc.fixturenames:
        abox_list = [p for p in glob(CQ_ABOX.as_posix() + "/**/*.rq", recursive=True)]
        metafunc.parametrize("cq_abox_path", abox_list)
    if "cq_tbox_path" in metafunc.fixturenames:
        tbox_list = [p for p in glob(CQ_TBOX.as_posix() + "/**/*.txt", recursive=True)]
        metafunc.parametrize("cq_tbox_path", tbox_list)


def check_abox(query, ontology, tmp):
    """Check competency question against the given ontology

    Args:
        conclusion (str): A filepath to the competency question.
        premise (str): A filepath to the reference ontology.

    Raises:
        RuntimeError: If calling ROBOT raises an error this will be raised as a RuntimeError.

    Returns:
        (boolean): Returns True if the competency question was sucessfully checked against the ontology.
    """
    query = Path(query).as_posix()
    instance_check = query.replace(
        CQ_ABOX.as_posix(), INSTANCE_PATH.as_posix()
    ).replace(".rq", ".ttl")
    if Path(instance_check).exists():
        instance_input = f" --input {instance_check} "
    else:
        instance_input = ""
    query_call = (
        f"{JAVA_PATH} -jar {ROBOT_JAR} merge --input {ontology} {instance_input} "
        + f"--catalog {CATALOG_PATH.as_posix()} "
        + 'reason --reasoner hermit --axiom-generators "PropertyAssertion" '
        + f"query --format ttl --query {query} {tmp.as_posix()}"
    )
    response = sp.call(query_call)
    if response != 0:
        raise RuntimeError(f"Response: {response} Call: {query_call}")
    with open(f"{tmp}", "r") as f:
        result = {"true": True, "false": False}.get(f.readline(), None)
        if result is None:
            raise RuntimeError(
                f"The query did not return a boolean. Call: {query_call}"
            )

    assert result, f"Question {query} was not satisfied. Call: {query_call}"


def check_tbox(conclusion, premise, tmp):
    """Check competency question against the given ontology

    Args:
        conclusion (str): A filepath to the competency question.
        premise (str): A filepath to the reference ontology.

    Raises:
        RuntimeError: If calling ROBOT raises an error this will be raised as a RuntimeError.

    Returns:
        (boolean): Returns True if the competency question was sucessfully checked against the ontology.
    """
    conclusion = Path(conclusion).as_posix()
    with open(conclusion, "r") as axf:
        axiom = axf.read()
    query_call = (
        f"{JAVA_PATH}  -jar {ROBOT_JAR} merge --input {premise} "
        + f"--catalog {CATALOG_PATH.as_posix()} "
        + f"explain --mode entailment --axiom {axiom} --explanation {tmp.as_posix()}"
    )
    response = sp.call(query_call)
    if response != 0:
        raise RuntimeError(f"Response: {response} Query: {axiom}")
    # with open(f"{tmp}", "r") as f:
    #     result = {"true": True, "false": False}.get(f.readline(), None)
    #     if result is None:
    #         raise RuntimeError("The query did not return a boolean.")

    # assert result, f"Question {conclusion} was not satisfied."


def test_abox(
    cq_abox_path,
    tmp_path_factory,
):
    """Metatest to produce competency question tests."""
    tmppath = tmp_path_factory.mktemp("data") / "test.ttl"
    check_abox(cq_abox_path, ONTOLOGY_PATH, tmppath)


def test_tbox(
    cq_tbox_path,
    tmp_path_factory,
):
    """Metatest to produce competency question tests."""
    tmppath = tmp_path_factory.mktemp("data") / "explanation.md"
    check_tbox(cq_tbox_path, ONTOLOGY_PATH, tmppath)
