# Quick smoke test for RTLGenerator.
# For more functionality testing please see test_top_agent.py
import argparse
import os

from mage.benchmark_read_helper import (
    TypeBenchmark,
    TypeBenchmarkFile,
    get_benchmark_contents,
)
from mage.gen_config import get_llm, set_exp_setting
from mage.log_utils import get_logger
from mage.rtl_generator import RTLGenerator
from mage.token_counter import TokenCounter, TokenCounterCached

logger = get_logger(__name__)

args_dict = {
    "provider": "ollama",
    "model": "qwen2.5-coder:0.5b",
    # "model": "claude-3-7-sonnet@20250219",
    # "model": "gemini-2.0-flash-001",
    # "model": "claude-3-7-sonnet-20250219",
    # "model": "gpt-4o-2024-08-06",
    # "filter_instance": "^(Prob070_ece241_2013_q2|Prob151_review2015_fsm)$",
    "filter_instance": "^(Prob011_norgate)$",
    # "filter_instance": "^(.*)$",
    "type_benchmark": "verilog_eval_v2",
    "path_benchmark": "./verilog-eval",
    "run_identifier": "your_run_identifier",
    "n": 1,
    "temperature": 0.85,
    "top_p": 0.95,
    "max_token": 8192,
    "use_golden_tb_in_mage": True,
    "key_cfg_path": "./key.cfg",
    "request_timeout": 60.0,
}


def main():
    args = argparse.Namespace(**args_dict)
    llm = get_llm(
        model=args.model,
        cfg_path=args.key_cfg_path,
        max_token=args.max_token,
        provider=args.provider,
    )
    token_counter = (
        TokenCounterCached(llm)
        if TokenCounterCached.is_cache_enabled(llm)
        else TokenCounter(llm)
    )
    set_exp_setting(temperature=args.temperature, top_p=args.top_p)
    type_benchmark = TypeBenchmark[args.type_benchmark.upper()]

    rtl_gen = RTLGenerator(token_counter)
    spec_dict = get_benchmark_contents(
        type_benchmark,
        TypeBenchmarkFile.SPEC,
        args.path_benchmark,
        args.filter_instance,
    )
    golden_tb_path_dict = get_benchmark_contents(
        type_benchmark,
        TypeBenchmarkFile.TEST_PATH,
        args.path_benchmark,
        args.filter_instance,
    )
    for key, spec in spec_dict.items():
        rtl_gen.reset()
        logger.info(spec)
        testbench_path = golden_tb_path_dict.get(key)
        if not testbench_path:
            logger.error(f"Testbench path not found for {key}")
            continue
        with open(testbench_path, "r") as f:
            testbench = f.read()
        # set output path to tmp
        rtl_path = f"./output_{key}_rtl.sv"
        is_pass, code = rtl_gen.chat(
            input_spec=spec,
            testbench=testbench,
            interface=None,
            rtl_path=rtl_path,
            enable_cache=True,
        )
        logger.info(is_pass)
        logger.info(code)
        # remove the generated RTL file
        os.remove(rtl_path)


if __name__ == "__main__":
    main()
