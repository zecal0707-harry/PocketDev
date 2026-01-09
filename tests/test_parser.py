import os
from src.parser import parse_comment

def test_basic_command():
    body = "/oc fix login bug"
    result = parse_comment(body)
    assert result is not None
    assert result['instruction'] == "fix login bug"
    assert result['model'] == "gemini"

def test_whitespace_command():
    body = "/oc    optimize database   "
    result = parse_comment(body)
    assert result is not None
    assert result['instruction'] == "optimize database"

def test_multiline_command():
    body = "/oc \nrefactor\nauth module"
    result = parse_comment(body)
    assert result is not None
    assert result['instruction'] == "refactor\nauth module"

def test_model_flag():
    body = "/oc --model gpt4 generate tests"
    result = parse_comment(body)
    assert result is not None
    assert result['instruction'] == "generate tests"
    assert result['model'] == "gpt4"

def test_no_trigger():
    body = "Please fix the bug"
    result = parse_comment(body)
    assert result is None

def test_empty_instruction():
    body = "/oc"
    result = parse_comment(body)
    assert result is None

def test_trigger_not_at_start_of_line():
    body = "hello /oc world"
    result = parse_comment(body)
    assert result is None

def test_trigger_multiline_start():
    body = "hello\n/oc world"
    result = parse_comment(body)
    assert result is not None
    assert result['instruction'] == "world"
