<h1 align="center">
<img src="bonsai_dark_long.png" width="800">
</h1><br>

# Bonsai: A Minimalist Directory Tree CLI Tool

## Overview
Bonsai is a command-line interface (CLI) tool designed for working with directory structures in a clear, compact, and visual way. It allows users to generate directory trees, save them as JSON files, load them from JSON, and compute relative paths between directories. The name "Bonsai" reflects the tool's ability to take something complex, like a filesystem, and represent it in an organized and elegant manner.

## Features
- **Visualize Directory Trees**: Generate and display the structure of directories with optional details like file permissions and file sizes.

- **Export to JSON**: Save the directory tree structure as a JSON file for later use or sharing.

- **Load from JSON**: Load a directory tree from a JSON file and visualize it.

- **Relative Paths**: Compute the relative path between two directories.

## Installation
1. Clone the repository:
```bash
git clone https://github.com/abhi-pixel1/bonsai.git
```
2. Install the tool using pip:
```bash
pip install .
```

## Usage
The Bonsai CLI includes the following commands:
1. ### `tree`
Generates and displays the directory tree for a given directory.

#### Syntax:
```bash
bonsai tree [DIRECTORY_PATH] [OPTIONS]
```
#### Arguments:

- `DIRECTORY_PATH`: The directory for which the tree should be generated (required).

#### Options:

- `-p`, `--show-permissions`: Include file permissions in the tree output.

- `-s`, `--show-size`: Include file sizes in the tree output.

#### Example:
```bash
bonsai tree ./my_directory -p -s
```

2. ### `save-tree`
Saves the directory tree structure of a given directory to a JSON file.

#### Syntax:
```bash
bonsai save-tree [DIRECTORY_PATH] [OUTPUT_FILE]
```

#### Arguments:

- `DIRECTORY_PATH`: The directory for which the tree should be saved (required).
- `OUTPUT_FILE`: The file where the JSON output should be saved. Must have a .json extension.

#### Example:

```bash
bonsai save-tree ./my_directory tree.json
```

3. ### `jtree`
Loads a directory tree structure from a JSON file and displays it.

#### Syntax:
```bash
bonsai jtree [JSON_FILE] [OPTIONS]
```

#### Arguments:

- `JSON_FILE`: Path to the JSON file containing the directory tree structure (required).

#### Options:

- `-p`, `--show-permissions`: Include file permissions in the tree output.
- `-s`,`--show-size`:  Include file sizes in the tree output.

#### Example:

```bash
bonsai jtree tree.json -p -s
```

4. ### `relative`
Calculates and displays the relative path between two directories.

#### Syntax:
```bash
bonsai relative [DESTINATION_PATH] [BASE_PATH]
```

#### Arguments:

- `DESTINATION_PATH`: The target directory.
- `BASE_PATH`: The starting directory.

#### Example:

```bash
bonsai relative ./my_directory ./another_directory
```

## Contributers:
<a href="https://github.com/othneildrew/Best-README-Template/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=abhi-pixel1/bonsai" alt="contrib.rocks image" />
</a>

## License

This project is licensed under the MIT License. See the LICENSE file for details.

