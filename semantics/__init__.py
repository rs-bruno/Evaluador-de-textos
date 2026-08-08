from . import DerivationRules 
from . import Words
import importlib.resources
from math import sqrt

__all__ = [
    'DerivationRules',
    'Words',
    'primitive',
    'richness',
]

# Paths definitions
base_words = r'palabras.txt'
sus_adj = r'sus_adj.txt'
reg_verb = r'reg_verb.txt'
irreg_verb_inf = r'irreg_verb_inf.txt'
irreg_verb_conj = r'irreg_verb_conj.txt'

resources = {
    base_words: None,
    sus_adj: None,
    reg_verb: None,
    irreg_verb_inf: None,
    irreg_verb_conj: None,
}

pkgRoot = importlib.resources.files(anchor=__name__)
txtTraversable = None
for subt in pkgRoot.iterdir():
    if (subt.name == 'txt'):
        txtTraversable = subt
        break
paths = list(resources.keys())
for text in txtTraversable.iterdir():
    if paths.count(text.name):
        resources[text.name] = text.open(encoding="UTF-8")

# Define predicates and generators for comprehension derivation rules
def predSufAble(word):
    if len(word) < 5:
        return False
    suf = word[len(word)-4:]
    if (suf == "able"):
        return True
    return False
def genSufAble(word):
    base = word[:len(word)-4]
    return [base + "abilidad"]

# Define derivation rules used to generate the final word set
rules = [
    DerivationRules.SingleFileExtensionRule(resources[sus_adj], 4),
    DerivationRules.SingleFileExtensionRule(resources[reg_verb], 53),
    DerivationRules.DoubleFileExtensionRule(resources[irreg_verb_inf], resources[irreg_verb_conj]),
    DerivationRules.ComprehensionRule(predSufAble, genSufAble),
]

words = {x: Words.WordNode(x) for x in [y.strip() for y in resources[base_words]]}

for rule in rules:
    rule.derive(words)

for path, resource in resources.items():
    resource.close()

totalWordCount = len(words)
primitiveWordCount = len([1 for x, v in words.items() if v.parentNode == None])

def test():
    print(totalWordCount)
    print(primitiveWordCount)

def primitive(word):
    """ For a word, returns its primitive word. 
    
    Args:
        word: Word of the dictionary.
    
    Returns:
        The primitive word for the word arg, or None if the word arg insn't in the dictionary.
    """
    if (word not in words):
        return None
    node = words[word]
    if (node.parentNode == None):
        return word
    elif (node.parentNode.text == word):
        return word
    else:
        return primitive(node.parentNode.text)

def noAlphaToSpace(line):
    buff = ''
    for char in line:
        if not char.isalpha():
            buff = buff + ' '
        else:
            buff = buff + char
    return buff


class Richness:
    sintactic = (100, 1)
    semantic = (100, 1)
    def __init__(self, sintactic, semantic):
        self.sintactic = sintactic
        self.semantic = semantic
    def getUsedWords(self):
        return self.sintactic[0]
    def getTotalWords(self):
        return self.sintactic[1]
    def getUsedPrimitives(self):
        return self.semantic[0]
    def getTotalPrimitives(self):
        return self.semantic[1]
    def getSintacticRichness(self):
        return 100 * self.sintactic[0] / self.sintactic[1]
    def getSemanticRichness(self):
        return 100 *  self.semantic[0] / self.semantic[1]

class BookDetails:
    bookLength = 0
    richness = None
    def __init__(self, len, rich):
        self.bookLength = len
        self.richness = rich
    def getDifficultyAndEffort(self):
        if self.bookLength <= 0:
            return 0
        difficulty = (self.richness.getUsedPrimitives() / self.richness.getUsedWords())
        effort = difficulty * self.bookLength
        ret = {
            "difficulty": difficulty,
            "effort": effort,
        }
        return ret

def evaluate(textFile):
    assert(not textFile.closed)
    textFile.seek(0)
    bookLength = 0
    usedWords = set()
    for line in textFile:
        cleanLine = noAlphaToSpace(line)
        lineWords = [word.lower() for word in cleanLine.split()]
        bookLength += len(lineWords)
        usedWords.update(lineWords)
    knownWords = {word for word in usedWords if word in words}
    usedPrimitives = {primitive(word) for word in knownWords}
    sintacticRichness = (len(knownWords), totalWordCount)
    semanticRichness = (len(usedPrimitives), primitiveWordCount)
    return BookDetails(bookLength, Richness(sintacticRichness, semanticRichness))
