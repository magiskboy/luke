<p align="center">
  <img width="420px" src="https://i.ibb.co/0BPYdRk/luke.png" alt='py-luke'>
</p>
<p align="center">
    <em>Working on OpenAPI easily.</em>
</p>
<p align="center">
    <a href="https://github.com/magiskboy/luke/actions">
        <img src="https://github.com/magiskboy/luke/actions/workflows/test-suite.yml/badge.svg" alt="Build Status">
    </a>
    <a href="https://app.codecov.io/gh/magiskboy/luke">
        <img src="https://img.shields.io/codecov/c/github/magiskboy/luke" alt="Code coverage">
    </a>
    <a href="https://pypi.org/project/py-luke/">
        <img src="https://img.shields.io/pypi/dd/py-luke" alt="Download PyPi">
    </a>
    <a href="https://github.com/magiskboy/luke/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/magiskboy/luke" alt="MIT">
    </a>
    <a href="https://pypi.org/project/py-luke/">
        <img src="https://img.shields.io/pypi/pyversions/py-luke" alt="Py version">
    </a>
    <a href="https://pypi.org/project/py-luke/">
        <img src="https://img.shields.io/pypi/v/py-luke" alt="PyPi version">
    </a>
</p>


## Features

Some of main features:

- Create a mock server for OpenAPI document
- Validate OpenAPI document with readable error messages
- Bundle OpenAPI fragments into the single document

py-luke supports both json and yaml type. Besides, you can also open file via path or URL.

## Installation

You can install py-luke from PyPi or Docker

```bash
$ pip install py-luke
$ docker run nguyenkhacthanh/luke:latest
```

## Usage

```bash
$ luke mock https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/petstore.yaml
```

or

```bash
$ docker run nguyenkhacthanh/latest validate https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/petstore.yaml
$ docker run -p8000:8000 nguyenkhacthanh/luke:latest mock https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/petstore.yaml
```
