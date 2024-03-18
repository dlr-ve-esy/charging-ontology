from glob import glob
import subprocess as sp
from pathlib import Path
import os
import shutil


CWD = os.getcwd()
with open(Path(CWD).joinpath("VERSION").as_posix()) as version_file:
    __version__ = version_file.readlines()[0].strip()

ROBOT_JAR = Path(CWD).joinpath("robot.jar").as_posix()
CATALOG_PATH = Path(CWD).joinpath("src/catalog-v001.xml")
CQ_ABOX = Path(CWD).joinpath("tests/cq_abox")
CQ_TBOX = Path(CWD).joinpath("tests/cq_tbox")
INSTANCE_PATH = Path(CWD).joinpath("tests/cq_instances")
JAVA_PATH = Path(shutil.which("java")).as_posix()

BUILD_PATH = (
    Path(CWD)
    .joinpath("build/chio")
    .joinpath(f"{__version__}")
    .joinpath("chio-full.ttl")
)
BUILD_MODE = BUILD_PATH.exists()

if BUILD_MODE:
    ONTOLOGY_PATH = BUILD_PATH
else:
    ONTOLOGY_PATH = Path(CWD).joinpath("src").joinpath("chio.ttl").as_posix()


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
        instance_input = ["--input", f"{instance_check}"]
    else:
        instance_input = []
    if BUILD_MODE:
        catalog_string = []
    else:
        catalog_string = ["--catalog", f"{CATALOG_PATH.as_posix()}"]
    query_call = (
        [
            f"{JAVA_PATH}",
            "-jar",
            f"{ROBOT_JAR}",
            "merge",
            "--input",
            f"{ontology}",
        ]
        + instance_input
        + catalog_string
        + ["reason", "--reasoner", "hermit", "--axiom-generators", "PropertyAssertion"]
        + ["query", "--format", "ttl", "--query", f"{query}", f"{tmp.as_posix()}"]
    )
    p = sp.Popen(
        query_call,
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
    )
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    if len(err) == 0:
        return output.decode("utf-8")
    else:
        raise RuntimeError(f"{err}")


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
    if BUILD_MODE:
        catalog_string = []
    else:
        catalog_string = ["--catalog", f"{CATALOG_PATH.as_posix()}"]
    query_call = (
        [f"{JAVA_PATH}", "-jar", f"{ROBOT_JAR}", "merge", "--input", f"{premise}"]
        + catalog_string
        + [
            "explain",
            "--mode",
            "entailment",
            "--axiom",
            f"{axiom}",
            "--explanation",
            f"{tmp.as_posix()}",
        ]
    )
    p = sp.Popen(
        query_call,
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
    )
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    if len(err) == 0:
        return output.decode("utf-8")
    else:
        raise RuntimeError(f"{err}")


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
