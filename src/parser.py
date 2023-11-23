#!/usr/bin/env python3
import argparse
import json
import logging
import re

QUESTION_HEADER_REGEX = r"^([TGE]\d\w\d\d) \((\w)\)(.*)"
QUESTION_FOOTER_REGEX = r"^~~$|^\s*$"


class NCVECQuestionParser():
    def __init__(self, input_file):
        self.lines = []
        self.count_deleted = 0

        self.stage1_read_input(input_file)
        self.stage2_chunk_question_blocks()
        self.stage3_parse_question_blocks()

        count_qblocks = len(self.qblocks)
        count_questions = len(self.questions)
        logging.info("QuestionParser initialized")
        logging.info(f"Found {count_qblocks} question blocks")
        logging.info(f"Found {self.count_deleted} questions marked DELETED")
        logging.info(f"Parsed {count_questions} question blocks")

    def stage1_read_input(self, input_file):
        logging.info(f"Reading input file: {input_file}")

        self.lines = []

        # Read lines from the input file
        with open(input_file, "r", encoding="utf-8") as fin:
            self.lines = fin.readlines()
            self.lines = [x.rstrip() for x in self.lines]

        # Squash non-ascii characters
        self.lines = [self._sanitize(line) for line in self.lines]

    def _sanitize(self, string):
        return "".join([x for x in string if ord(x) >= 32 and ord(x) <= 126])

    def stage2_chunk_question_blocks(self):
        logging.info("Chunking into question blocks")

        self.questions = []
        self.qblocks = []
        lines = self.lines[:]

        while len(lines):
            qblock = []

            try:
                while not re.match(QUESTION_HEADER_REGEX, lines[0]):
                    discard = lines.pop(0)
                    if not len(discard):
                        discard = "<blank line>"
                    logging.debug(f"DISCARD: {discard}")
                while not re.match(QUESTION_FOOTER_REGEX, lines[0]):
                    qline = lines.pop(0)
                    qblock.append(qline)
                    logging.debug(f"QLINE: {qline}")
            except IndexError:
                if len(qblock):
                    raise RuntimeError("Found unterminated question block")
                break

            self.qblocks.append(qblock)

    def stage3_parse_question_blocks(self):
        logging.info("Parsing question blocks")

        for qblock in self.qblocks:
            self._parse_qblock(qblock)

    def _parse_qblock(self, qblock):
        header_peek = qblock[0]
        if "DELETED" in header_peek:
            self.count_deleted += 1
            logging.info(f"Skipping {header_peek}")
            return

        ############################################################
        # Construct field values for the question record
        ############################################################

        header = qblock.pop(0)
        qtext = qblock.pop(0)
        options_orig = qblock[:]

        result = re.match(QUESTION_HEADER_REGEX, header)
        if not result:
            raise RuntimeError(f"Invalid question header {header}")

        question_id = result.group(1)
        refs = result.group(3).strip()
        answer = result.group(2)
        answer_idx = self._answer_idx(answer)

        # TODO(sbostick):
        # This subsection is unnecessary; experimenting with how I might
        # randomize the inputs and still be able to check answers either
        # in front-end or back-end. Prefer not to leak the answers into
        # the markup.
        options_parsed = []
        for opt in options_orig:
            result = re.match(r"^(\w)\. (.*)", opt)
            if not result:
                raise RuntimeError(f"Invalid option formatting [{opt}]")
            letter = result.group(1)
            text = result.group(2)
            option_idx = self._answer_idx(letter)
            correct = bool(option_idx == answer_idx)
            options_parsed.append({
                "letter": letter,
                "option_idx": option_idx,
                "correct": correct,
                "text": text})

        ############################################################
        # Store the structured record
        ############################################################

        self.questions.append({
            "header": header,
            "qtext": qtext,
            "options_orig": options_orig,
            "options_parsed": options_parsed,
            "answer": answer,
            "answer_idx": answer_idx,
            "question_id": question_id,
            "refs": refs})

    def _answer_idx(self, key):
        if not hasattr(self, "answer_idx_decoder"):
            keys = list(map(chr, range(ord("A"), ord("Z") + 1)))
            vals = list(range(0, 27))
            self.answer_idx_decoder = dict(zip(keys, vals))

        return self.answer_idx_decoder[key.upper()]

    def output_json(self, output_file):
        with open(output_file, "w", encoding="utf-8") as fout:
            fout.write(json.dumps(self.questions, sort_keys=True, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file")
    parser.add_argument("--output-file")
    parser.add_argument("--verbose",
                        action=argparse.BooleanOptionalAction,
                        default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    qpx = NCVECQuestionParser(args.input_file)
    qpx.output_json(args.output_file)
