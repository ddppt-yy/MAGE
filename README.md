# MAGE: A Multi-Agent Engine for Automated RTL Code Generation

You can learn more on our Arxiv Paper: https://arxiv.org/abs/2412.07822.
MAGE is an open-source multi-agent LLM RTL code generator.

![DAC-overview](fig/DAC-overview.png)

## Environment Set Up

### 1.> To install the repo itself:
```
git clone https://github.com/stable-lab/MAGE.git
# To get submodules at the same time
git clone --recursive https://github.com/stable-lab/MAGE.git
cd MAGE

# Install conda first if it's not on your machine like "apt install conda"
# To confirm successful installation of conda, run "conda --version"
# Continue after successfully installed conda
conda create -n mage python=3.11
conda activate mage

# Install the repo as a package.
# If want to editable install as developer,
# please check development guide below.
pip install .
```

### 2.>To set api key：
You can either:
1. Set "OPENAI_API_KEY", "ANTHROPIC_API_KEY" or other keys in your env variables
2. Create key.cfg file. The file should be in format of:

```
OPENAI_API_KEY= 'xxxxxxx'
ANTHROPIC_API_KEY= 'xxxxxxx'
VERTEX_SERVICE_ACCOUNT_PATH= 'xxxxxxx'
VERTEX_REGION= 'xxxxxxx'
```

### To install iverilog {.tabset}
You'll need to install [ICARUS verilog](https://github.com/steveicarus/iverilog) 12.0
For latest installation guide, please refer to [iverilog official guide](https://steveicarus.github.io/iverilog/usage/installation.html)

#### Ubuntu (Local Compilation)
```
apt install -y autoconf gperf make gcc g++ bison flex
```
and
```
$ git clone https://github.com/steveicarus/iverilog.git && cd iverilog \
        && git checkout v12-branch \
        && sh ./autoconf.sh && ./configure && make -j4\
$ sudo make install
```
#### MacOS
```
brew install icarus-verilog
```

#### Version confirmation of iverilog
Please confirm the iverilog version is v12 by running
```
iverilog -v
```

First line of output is expected to be:
```
Icarus Verilog version 12.0 (stable) (v12_0)
```

### 3.>  Verilator Installation

```
# By apt
sudo apt install verilator

# By Compilation
git clone https://github.com/verilator/verilator
cd verilator
autoconf
export VERILATOR_ROOT=`pwd`
./configure
make -j4
```

### 4.> Pyverilog Installation

```
# pre require
pip3 install jinja2 ply

git clone https://github.com/PyHDI/Pyverilog.git
cd Pyverilog
# must to user dir, or error because no root
python3 setup.py install --user
```

### 5.> To get benchmarks

```
[verilog-eval](https://github.com/NVlabs/verilog-eval)
```

```
git submodule update --init --recursive
```

## Run Guide
```
python tests/test_top_agent.py
```

Run arguments can be set in the file like:

```
args_dict = {
    "provider": "anthropic",
    "model": "claude-3-5-sonnet-20241022",
    # "model": "gpt-4o-2024-08-06",
    # "filter_instance": "^(Prob070_ece241_2013_q2|Prob151_review2015_fsm)$",
    "filter_instance": "^(Prob011_norgate)$",
    # "filter_instance": "^(.*)$",
    "type_benchmark": "verilog_eval_v2",
    "path_benchmark": "../verilog-eval",
    "run_identifier": "your_run_identifier",
    "n": 1,
    "temperature": 0.85,
    "top_p": 0.95,
    "max_token": 8192,
    "use_golden_tb_in_mage": True,
    "key_cfg_path": "key.cfg",
}
```
Where each argument means:
1. provider: The api provider of the LLM model used. e.g. anthropic-->claude, openai-->gpt-4o
2. model: The LLM model used. Support for gpt-4o and claude has been verified.
3. filter_instance: A RegEx style instance name filter.
4. type_benchmark: Support running verilog_eval_v1 or verilog_eval_v2
5. path_benchmark: Where the benchmark repo is cloned
6. run_identifier: Unique name to disguish different runs
7. n: Number of repeated run to execute
8. temperature: Argument for LLM generation randomness. Usually between [0, 1]
9. top_p: Argument for LLM generation randomness. Usually between [0, 1]
10. max_token: Maximum number of tokens the model is allowed to generate in its output.
11. key_cfg_path: Path to your key.cfg file. Defaulted to be under MAGE


## Development Guide

Run editable install and setup pre-commit like:
```
pip install -e . --config-settings editable_mode=compat
pre-commit install
```
