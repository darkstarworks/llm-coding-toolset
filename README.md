> [!TIP]
> # LLM-Coding Toolset <br>
>   
> Is a Python application that provides a set of tools to assist developers <br>
> in working with Large Language Models (LLMs). It includes various features: <br>

## Features

- **Folder Structure Viewer**: Visualize and export folder structures with customizable depth.
- **Line Number Adder**: Add line numbers to code snippets, with support for finding snippets within larger files.
- **Diff Viewer**: Compare two text inputs and visualize the differences.
- **Theme Support**: Choose between light and dark themes.
- **Settings Management**: Customize default behaviors and appearance.
- **Auto-update Checker**: Stay up-to-date with the latest version.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/darkstarworks/llm-coding-toolset.git
   cd llm-coding-toolset
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the LLM-Coding Toolset:

```
python -m src.main
```

Or, if you've installed it as a package:

```
llm-coding-toolset
```

## Dependencies

- PyQt5 (v5.15.11)
- pyperclip (v1.9.0)
- requests (v2.32.3)

For a complete list of dependencies, see `requirements.txt`.

## Contributing

**Contributions are welcome! Feel free to submit a Pull Request.** <br>
*After reading the guidelines, in: [CONTRIBUTING.md](CONTRIBUTING.md)* <br>
Thank you :)

## License

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/">
  <span style="vertical-align:sub;">
    <a property="dct:title" rel="cc:attributionURL" href="https://github.com/darkstarworks/llm-coding-toolset">LLM-Coding Toolset</a> by 
      <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/darkstarworks">darkstarworks</a> is licensed under 
      <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer">CC BY-NC-SA 4.0 </span><span style="vertical-align:bottom;"><img style="height:22px;padding:3px;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt="CC"><img style="height:22px;padding:3px;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt="BY"><img style="height:22px;padding:3px;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt="NC"><img style="height:22px;padding:3px;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt="SA"></a>
      </span>
    </a>
  </span>
</p>
