# EagleVision

Tool to identify and report

- Extract the source code to dataframe

- Pattern checking

- Similarity checking

- Cyclomatic complexity checking

- Repository statistics like, Type of file, LOC, Comments, Code etc.

## Dependencies

- python 3.8 : 64 bit  

- python packages (functiondefextractor, similarity-processor, lizard)  

- cloc package `npm i -g cloc@2.6.0` `https://www.npmjs.com/package/cloc`

- third party packages [Ctags, grep]

## Installation
  
[INSTALL.md](INSTALL.md)

## Usage

### Commandline

```sh
>>>python -m eaglevision --p "path\to\input\json"
```

- sample json input,  

```sh
[
  {
    "path": "repo/path",
    "run_pattern_match":true,
    "run_similarity":true,
    "extraction_annotation": null,
    "extraction_delta": null,
    "extraction_exclude": "*/test_resource/*",
    "pattern_match": ["assert"],
    "pattern_seperator": ["("],
    "similarity_range": "70,100",
    "run_cloc_metric":true,
    "cloc_args": "--exclude-dir=src --exclude-ext=*.cpp,*.java",
    "run_cyclomatic_complexity":true,
    "cyclo_args": "-l java  -l python",
    "cyclo_exclude": ["*.cpp","*.java"],
    "report_folder": null
  }
]
```

Note:

All the inputs are taken from the json file

1. Do not forget to have the json as list `[...]`

2. Make sure `pattern_match` and `pattern_seperator` is of same length list
 if you are not interested in any `pattern_seperator` for s specific
 `pattern_match` , mark it `null` in `pattern_seperator`

3. Make sure mark it `null` if a string or list parameter is not used

4. Make sure mark it `true/false` for bool type

```sh
refer https://www.npmjs.com/package/cloc for cloc args
refer https://pypi.org/project/lizard/ for cyclo args
refer https://pypi.org/project/functiondefextractor/ for extraction_exclude
refer https://pypi.org/project/similarity-processor/ for similarity
```

### Output
  
- Output will be available in same folder as `path` given in json under  `EagleVisionReport`

## Contact

[MAINTAINERS.md](MAINTAINERS.md)  

## License

[License.md](LICENSE.md)
