#!/usr/bin/env python

import os
import sys
import subprocess


def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def capture_command(command):
    ''' run command and captures output '''
    try:
        res = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print("command returned error code " + str(e.returncode))
        print("    - output: " + e.output)
        res = e.output

    return res


def passthru_command(command):
    ''' run command and output on screen '''
    subprocess.call(command, shell=True)

rootDir = os.path.dirname(os.path.realpath(__file__))

# TODO take 1 parameter, formula name
formulaName = "giflib"

try:
    formula = get_class("formulas." + formulaName + "." + formulaName)
except ImportError:
    print("ERROR: No such formula " + formulaName)
    sys.exit()

if formula.scm != "git":
    print("ERROR: unsupported scm: " + formula.scm)
    sys.exit()

print("### " + formulaName)

formulaPath = ".cache/" + formulaName

gitPath = formulaPath + "/.git"
if os.path.isdir(gitPath):
    # TODO if dir exist, do a "git pull" ? also make sure it is pristine
    print("Checkout found at " + gitPath + ", TODO do update?")
else:
    print("Checking out " + formula.origin + " ...")

    gitClone = "git clone " + formula.origin + " .cache/" + formulaName
    capture_command(gitClone)

# set current working dir to formulaPath
os.chdir(formulaPath)
# print("changed cwd to " + os.getcwd())

# TODO support multiple targets somehow
fuzzTarget = formula.targets[0]

if not os.path.isfile(fuzzTarget):
    # if target not found, perform clean + build
    for cleanCmd in formula.clean:
        print("CLEAN # " + cleanCmd)
        capture_command(cleanCmd)

    for buildCmd in formula.build:
        print("BUILD # " + buildCmd)
        capture_command(buildCmd)

if not os.path.isfile(fuzzTarget):
    print("ERROR cant find target " + fuzzTarget + ", giving up")
    sys.exit()

print("Found " + fuzzTarget + ", ready to fuzz")

# TODO prepare test cases from dataTypes list

aflInDir = rootDir + "/testcases/images/gif"
aflOutDir = rootDir + "/.fuzz-afl/" + formulaName
aflFuzzTarget = rootDir + "/" + formulaPath + "/" + fuzzTarget
fuzzCmd = "afl-fuzz -i " + aflInDir + " -o " + aflOutDir + " " + aflFuzzTarget
print("Executing: " + fuzzCmd)

passthru_command(fuzzCmd)