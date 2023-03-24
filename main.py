import json

from crawler import Crawler
import codecs

from source.Searcher import Searcher
from source.TfIdfGenerator import TfIdfGenerator
from source.Tokenizer import Tokenizer

isHomework_2 = False
isHomework_3 = False
isHomework_4 = True

if __name__ == '__main__':
    tokenizer = Tokenizer()
    if isHomework_2:
        tokens, lemmas = tokenizer.get_tokens_and_lemmas("output/pages/")

        out1 = codecs.open("output/tokens.txt", "w", "utf-8")
        for token in tokens:
            out1.write(token + "\n")
        out1.close()

        out2 = codecs.open("output/lemmas.txt", "w", "utf-8")
        for k, v in lemmas.items():
            out2.write(k)
            for t in v:
                out2.write(" " + t)
            out2.write("\n")
        out2.close()
    if isHomework_3:
        tokenizer = Tokenizer()
        lemmas_to_files = tokenizer.get_lemmas_to_files("output/pages/")

        json_string = json.dumps(lemmas_to_files, ensure_ascii=False)
        with codecs.open("output/inverted_index.json", "w", "utf-8") as outfile:
            outfile.write(json_string)

        searcher = Searcher()
        searcher.make()
    if isHomework_4:
        tfIdfGenerator = TfIdfGenerator()
        tfIdfGenerator.main()
