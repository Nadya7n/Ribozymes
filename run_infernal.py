#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 06.06.2021
# @author: Nadezhda Sorokina
# @contact: nadya7n@bk.ru

import argparse
import logging as log
import os

from tqdm import tqdm


def main(settings):
    """
    Function runs the Infernal
    :param settings: dict with parameters
            param1 (str): Fasta files directory.
            param2 (str): Cm-models files directory.
            param3 (str): Working directory.
            params4 (int): Number of threads.
            params5 (int): Verbosity
    :return: None
    """

    fasta_files_dir = settings["fasta"]
    cm_files_dir = settings["cm"]
    working_dir = settings["output"]
    threads = settings["threads"]
    verbone = settings["verbone"]

    list_of_command = os.path.join(working_dir, f"ribo2compute.list")

    if verbone == 2:
        log.basicConfig(filename=f"{working_dir}/infernal_debug.log", level=log.DEBUG)
    else:
        log.basicConfig(filename=f"{working_dir}/infernal.log", level=log.INFO)

    with open(list_of_command, "a+") as fw:
        for gid, fasta_file in enumerate(tqdm(os.listdir(fasta_files_dir))):
            if not fasta_file.endswith("fna"):
                continue
            id_genome = os.path.splitext(fasta_file)[0]

            for mid, cm_file in enumerate(os.listdir(cm_files_dir)):
                if not cm_file.endswith("cm"):
                    continue
                id_model = cm_file.split(".")[0]
                output = os.path.join(
                    working_dir, f"{id_model}/{id_genome}_{id_model}.out"
                )

                if os.path.exists(output):
                    log.error(f"--Error_1--\t{output}\talready exists")
                    continue

                path_to_model = os.path.join(cm_files_dir, cm_file)
                path_to_genome = os.path.join(fasta_files_dir, fasta_file)
                command = f"cmsearch --cpu {threads} {path_to_model} {path_to_genome} > {output}"
                fw.write(f"{command}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Write commands for running cmsearch Infernal, takes 4 arguments as input"
    )

    parser.add_argument("-f", "--fasta", help="Fasta input directory", required=True)
    parser.add_argument("-c", "--cm", help="Cm_model input directory", required=True)
    parser.add_argument("-o", "--output", help="Working directory", required=True)
    parser.add_argument("-t", "--threads", help="Number_of_threads", required=True)
    parser.add_argument(
        "-v",
        "--verbone",
        type=int,
        help="increase output verbosity:\n 0-level ERROR\n, 1-level INFO\n, 2-level DEBUG\n",
        default=0,
    )

    args = vars(parser.parse_args())

    settings = {
        "fasta": args["fasta"],
        "cm": args["cm"],
        "output": args["output"],
        "threads": args["threads"],
        "verbone": args["verbone"],
    }

    main(settings)
