# %%
import requests
from pathlib import Path
import subprocess as sp

ONTOLOGY_BASE = (
    "https://enterpriseintegrationlab.github.io/icity/Parking/doc/ontology.ttl"
)
# Change this path according to your setup.


ROBOT_PATH = "../../robot.jar"
TMP = "tmp"
Path(TMP).mkdir(exist_ok=True)

TARGET = Path(TMP).joinpath("Parking.ttl")
# %%
if not Path(TARGET).exists():
    with open(TARGET, "wb") as local:
        response = requests.get(ONTOLOGY_BASE)
        if response.status_code == 200:
            local.write(response.content)
else:
    print(f"The file {TARGET} already exists, you are good to go.")


# %%
def extract_subset(input: str, output: str, terms: str):
    """Call robot to do a subset extraction"""
    extract_call = (
        "java -jar {jar} extract "
        "--input {input} "
        "--method subset "
        "--term-file {term_file} "
        "--imports include "
        "--output {output}"
    )
    with open(Path("tmp").joinpath("temp.txt"), "w") as fp:
        for term in terms:
            fp.write(term + "\n")
    debug_string = extract_call.format(
        jar=Path(ROBOT_PATH).resolve().as_posix(),
        input=Path(input).resolve().as_posix(),
        term_file=Path("tmp").joinpath("temp.txt").resolve().as_posix(),
        # term_file_filter=Path("tmp").joinpath("temp.txt").resolve().as_posix(),
        output=Path(output).resolve().as_posix(),
    )
    code = sp.call(
        debug_string,
        shell=True,
    )
    if code != 0:
        print(debug_string)
        raise IOError(f"Something went wrong with call: {debug_string}")
    return code


# %%
def robot_convert(
    input: str,
    output: str,
    formt: str = "owx",
):
    """Call robot to do a convertion"""
    convert_call = (
        "java -jar {jar} merge "
        "--input {input} convert "
        "--output {output} "
        "--format {formt}"
    )
    debug_string = convert_call.format(
        jar=Path(ROBOT_PATH).resolve().as_posix(),
        input=Path(input).resolve().as_posix(),
        output=Path(output).resolve().as_posix(),
        formt=formt,
    )
    code = sp.call(
        debug_string,
        shell=True,
    )
    if code != 0:
        print(debug_string)
        raise IOError(f"Something went wrong with call: {debug_string}")
    return code


# %%
# For this to work imports have to be manually removed from the Parking
# ontology. Something is going wrong with robot
if not Path(TMP).joinpath("parking_space.ttl").exists():
    terms = [
        "http://ontology.eil.utoronto.ca/icity/Change/manifestationOf",
        "http://ontology.eil.utoronto.ca/icity/Parking/ParkingAreaPD",
        "http://ontology.eil.utoronto.ca/icity/Parking/ParkingArea",
        "http://ontology.eil.utoronto.ca/icity/Parking/ParkingSpace",
        "http://ontology.eil.utoronto.ca/icity/Parking/GreenVehicleParkingSpace",
        "http://ontology.eil.utoronto.ca/icity/Change/hasManifestation",
        "http://ontology.eil.utoronto.ca/icity/Parking/EVParkingSpace",
        "http://ontology.eil.utoronto.ca/icity/Parking/EVParkingPolicy",
        "http://ontology.eil.utoronto.ca/icity/Parking/hasParkingPolicy",
        "http://ontology.eil.utoronto.ca/icity/Parking/hasEVCharger",
        "http://ontology.eil.utoronto.ca/icity/Parking/EVCharger",
        "http://ontology.eil.utoronto.ca/icity/Parking/MediumEVCharger",
        "http://ontology.eil.utoronto.ca/icity/Parking/QuickEVCharger",
        "http://ontology.eil.utoronto.ca/icity/Parking/StandardEVCharger",
    ]
    extract_subset(
        input=TARGET,
        output=Path(TMP).joinpath("parking_space.ttl"),
        terms=terms,
    )
robot_convert("tmp/parking_space.ttl", "tmp/parking_space.owx")
# %%
