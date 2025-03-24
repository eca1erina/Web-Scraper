import requests
import re
import fitz  # PyMuPDF
from bs4 import BeautifulSoup


class TrieNode:
    def __init__(self):
        self.children = {}
        self.output = []
        self.fail = None


def build_automaton(keywords):
    root = TrieNode()

    for keyword in keywords:
        node = root
        for char in keyword:
            node = node.children.setdefault(char, TrieNode())
        node.output.append(keyword)

    queue = []
    for node in root.children.values():
        queue.append(node)
        node.fail = root

    while queue:
        current_node = queue.pop(0)
        for key, next_node in current_node.children.items():
            queue.append(next_node)
            fail_node = current_node.fail
            while fail_node and key not in fail_node.children:
                fail_node = fail_node.fail
            next_node.fail = fail_node.children[key] if fail_node else root
            next_node.output += next_node.fail.output

    return root


def search_text(text, keywords):
    root = build_automaton(keywords)
    result = {keyword: [] for keyword in keywords}

    current_node = root
    for i, char in enumerate(text):
        while current_node and char not in current_node.children:
            current_node = current_node.fail

        if not current_node:
            current_node = root
            continue

        current_node = current_node.children[char]
        for keyword in current_node.output:
            result[keyword].append(i - len(keyword) + 1)

    return result


class RedBlackTreeNode:
    def __init__(self, key, color="RED"):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    def __init__(self):
        self.TNULL = RedBlackTreeNode("", color="BLACK")
        self.root = self.TNULL

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert_fix(self, k):
        while k.parent.color == "RED":
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == "RED":
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.right_rotate(k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == "RED":
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.left_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "BLACK"

    def insert(self, key):
        node = RedBlackTreeNode(key)
        node.parent = None
        node.key = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = "RED"
        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right
        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        if node.parent is None:
            node.color = "BLACK"
            return
        if node.parent.parent is None:
            return
        self.insert_fix(node)

    def inorder_helper(self, node):
        if node != self.TNULL:
            self.inorder_helper(node.left)
            print(node.key)
            self.inorder_helper(node.right)

    def inorder(self):
        self.inorder_helper(self.root)


def fetch_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return ""


def extract_sentences(text):
    sentence_endings = re.compile(r"([.!?])")
    sentences = re.split(sentence_endings, text)
    sentences = [s.strip() + ending if i % 2 == 0 else ending for i, (s, ending) in enumerate(zip(sentences[::2], sentences[1::2]))]
    return [s for s in sentences if s.strip()]


def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text("text")
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""


def main():
    input_type = input("Do you want to scrape a URL or process a PDF file? (Enter 'url' or 'pdf'): ").strip().lower()

    if input_type == "url":
        url = input("Enter the URL to scrape: ")
        text = fetch_webpage(url)
    elif input_type == "pdf":
        pdf_path = input("Enter the path to the PDF file: ")
        text = extract_text_from_pdf(pdf_path)
    else:
        print("Invalid choice. Exiting.")
        return

    keywords = input("Enter keywords separated by space: ").split()

    sentences = extract_sentences(text)

    result = {}
    for sentence in sentences:
        matches = search_text(sentence, keywords)
        for keyword, positions in matches.items():
            if positions:
                if keyword not in result:
                    result[keyword] = []
                result[keyword].append((sentence, positions))

    rbt = RedBlackTree()
    for keyword, sentences_with_positions in result.items():
        for sentence, _ in sentences_with_positions:
            rbt.insert(sentence)

    print("\nSentences containing at least one keyword:\n")
    rbt.inorder()


if __name__ == "__main__":
    main()
