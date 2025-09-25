
<h1 align="center">
  <br>
  <a href="https://vantage6.ai"><img src="https://github.com/IKNL/guidelines/blob/master/resources/logos/vantage6.png?raw=true" alt="vantage6" width="350"></a>
</h1>

<h3 align=center> A Privacy Enhancing Technology (PET) Operations platform</h3>
<h3 align="center">

<!-- Badges go here-->



</h3>

<p align="center">
  <a href="#books-quickstart">Quickstart</a> •
  <a href="#project-structure">Project structure</a> •
  <a href="#gift_heart-join-the-community">Join the community</a> •
  <a href="#scroll-license">License</a> •
  <a href="#black_nib-code-of-conduct">Code of conduct</a> •
  <a href="#black_nib-references">References</a>
</p>

---

This repository is contains some basic session algorithms that run on the vantage6 platform. For more information on how to use vantage6, please visit the [vantage6 website](https://vantage6.ai).

The base code for this algorithm has been created via the
[v6-algorithm-template](https://github.com/vantage6/v6-algorithm-template)
template generator.

## Build algorithm image

Build and (optionally) push the algorithm image:
```bash
make image TAG=latest VANTAGE6_VERSION=5.0.0
# add PUSH_REG=true to also push
```

The Dockerfile installs dependencies with uv using the lockfile for reproducibility and then installs the project.

## Development quickstart

Local setup using uv:
```bash
# Create/refresh virtualenv and install deps from pyproject/uv.lock
uv sync

# Run the package (example: list available functions or run tests)
# if you want to add a dependency## Developing
```
