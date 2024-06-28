# README
## Generals information
The `src` folder contains the source code of our project. The source code is made of **7** scripts, **more information about
each script can be found directly in their sources files**:
- `main.py`, a small script to compute Euclidean distance between two images using **SMC** (using MPyC library)
- `serializing.py`, this script will extract all the face encodings of all the images in a directory and store them in a
*pickle* file. The *pickle* file will be the dataset used by the *benchmark* script and the *demo_server*. We do the
extraction of face encodings in this part and not in the other script to increase compute speed.
- `benchmark.py`, a benchmark script to test speed and a threshold value using MPyC
- `without_smc_benchmark.py`, a benchmark script to test speed and a threshold value **without** using MPyC
- `compare_lib.py`, very small script to compare the size of data generated between the *DeepFace* and *face_recognition*
library
- `demo_server.py` and `demo_server_backend.py`, the server part of a demonstrator that give an example of usage. This
demonstrator simulate a communication between a server and a client. The server has a database of faces of authorized
people whereas the client as the picture of one person. By doing an **SMC** the client and the server determine if the client's
face is recognized without never sharing the picture of the client nor the faces of the database.
- `demo_client.py` and `demo_client_backend.py`, the client side of the demonstrator. Must be started **after**
`demo_server.py`

A dedicated help page is available for each script (with the option `-h`). **Moreover, you can find more information at the beginning
of each script.**

**Launch those script directly in `src` folder**

### Notes
The client and the server of the demonstrator need to exchange the number of computation to process. This value correspond
to the size of the dataset. If the server is launch on another dataset that `data/serialized_150_prod.py` you will need to
change in `demo_client_backend.py` the call to `get_dataset_length` with the path to the dataset use for launching the server.

## Architecture
data: This folder contains all used datasets.
report: This folder contains generated reports in PDF format, along with their source files, if desired.
slides: This folder contains generated slides in PDF format, along with their source files, if desired.
src: This folder contains the source code files.
README.md: This file provides an overview of the project and the repository structure.
.gitignore: This file specifies the files and folders that should not be tracked by Git.
