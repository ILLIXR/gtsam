"""
Unit test for documentation generation
Author: Matthew Sklar
Date: May 2019
"""
import filecmp
import os
import os.path as path
import shutil
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import docs.parser.parse_doxygen_xml as parser
from docs.docs import ClassDoc, Doc, Docs, FreeDoc


tree_root = ET.Element('a')
tree_left = ET.SubElement(tree_root, 'b')
tree_right = ET.SubElement(tree_root, 1)
tree_leaf = ET.SubElement(tree_right, None)
tree_recursive = ET.SubElement(tree_left, tree_left)

a = ET.Element('a')
b = ET.SubElement(a, 'b')
c = ET.SubElement(b, 'c')
d = ET.SubElement(b, 'd')
d2 = ET.SubElement(d, 'd')


class TestDocument(unittest.TestCase):
    DIR_NAME = path.dirname(__file__)

    DOC_DIR = 'doc-test-files'
    OUTPUT_XML_DIR = 'actual-xml-generation'
    EXPECTED_XML_DIR = 'expected-xml-generation'

    DOC_DIR_PATH = path.abspath(path.join(DIR_NAME, DOC_DIR))
    OUTPUT_XML_DIR_PATH = path.abspath(path.join(DIR_NAME, OUTPUT_XML_DIR))
    EXPECTED_XML_DIR_PATH = path.abspath(path.join(DIR_NAME, EXPECTED_XML_DIR))

    def test_generate_xml(self):
        '''Test parse_xml.generate_xml'''
        shutil.rmtree(self.OUTPUT_XML_DIR_PATH, ignore_errors=True)
        parser.generate_xml(
            self.DOC_DIR_PATH, self.OUTPUT_XML_DIR_PATH, quiet=True)

        self.assertTrue(os.path.isdir(self.OUTPUT_XML_DIR_PATH))

        shutil.rmtree(path.join(self.OUTPUT_XML_DIR_PATH, 'xml'))
        parser.generate_xml(
            self.DOC_DIR_PATH, self.OUTPUT_XML_DIR_PATH, quiet=True)

        dircmp = filecmp.dircmp(
            self.OUTPUT_XML_DIR_PATH, self.EXPECTED_XML_DIR_PATH)

        self.assertTrue(not dircmp.diff_files and not dircmp.funny_files)

    def test_parse(self):
        docs = parser.ParseDoxygenXML(
            self.DOC_DIR_PATH, self.OUTPUT_XML_DIR_PATH).run()

        for class_name in docs.get_class_docs_keys_list():
            actual_tree_root = docs.get_class_docs(
                class_name).get_tree().getroot()
            expected_tree_root = ET.parse(class_name).getroot()

            self.assertEqual(
                ET.tostring(actual_tree_root), ET.tostring(expected_tree_root))


class TestDocTemplate(unittest.TestCase):
    class_doc_root = ClassDoc(tree_root)
    class_doc_left = ClassDoc(tree_left)
    class_doc_right = ClassDoc(tree_right)
    class_doc_leaf = ClassDoc(tree_leaf)
    class_doc_recursive = ClassDoc(tree_recursive)

    free_doc_root = ClassDoc(tree_root)
    free_doc_left = ClassDoc(tree_left)
    free_doc_right = ClassDoc(tree_right)
    free_doc_leaf = ClassDoc(tree_leaf)
    free_doc_recursive = ClassDoc(tree_recursive)

    CLASS_DOCS = {
        'Class_Root': tree_root,
        'Class_Left': tree_left,
        'Class_Right': tree_right,
        'Class_Leaf': tree_leaf,
        'Class_Recursive': tree_recursive,
    }

    FREE_DOCS = {
        'Free_Root': tree_root,
        'Free_Left': tree_left,
        'Free_Right': tree_right,
        'Free_Leaf': tree_leaf,
        'Free_Recursive': tree_recursive,
    }

    # ClassDoc
    def test_class_doc(self):
        '''Test the constructor in ClassDoc'''
        self.assertIs(self.class_doc_root.tree, tree_root)
        self.assertIs(self.class_doc_left.tree, tree_left)
        self.assertIs(self.class_doc_right.tree, tree_right)
        self.assertIs(self.class_doc_leaf.tree, tree_leaf)
        self.assertIs(self.class_doc_recursive.tree, tree_recursive)

    def test_class_doc_get_tree(self):
        '''Test the get_tree() method is ClassDoc'''
        self.assertIs(self.class_doc_root.get_tree(), tree_root)
        self.assertIs(self.class_doc_left.get_tree(), tree_left)
        self.assertIs(self.class_doc_right.get_tree(), tree_right)
        self.assertIs(self.class_doc_leaf.get_tree(), tree_leaf)
        self.assertIs(self.class_doc_recursive.get_tree(), tree_recursive)

    def test_class_doc_eq(self):
        '''Test ClassDoc.__eq__'''
        doc1 = ClassDoc(ET.ElementTree(a))
        doc2 = ClassDoc(ET.ElementTree(d))
        doc3 = ClassDoc(ET.ElementTree(d2))

        self.assertEqual(doc1, doc1)
        self.assertEqual(doc2, doc2)
        self.assertNotEqual(doc2, doc3)
        self.assertEqual(None, None)
        self.assertNotEqual(doc1, doc2)
        self.assertNotEqual(doc1, None)

    # FreeDoc
    def test_free_doc(self):
        '''Test the constructor in FreeDoc'''
        self.assertIs(self.free_doc_root.tree, tree_root)
        self.assertIs(self.free_doc_left.tree, tree_left)
        self.assertIs(self.free_doc_right.tree, tree_right)
        self.assertIs(self.free_doc_leaf.tree, tree_leaf)
        self.assertIs(self.free_doc_recursive.tree, tree_recursive)

    def test_free_doc_get_tree(self):
        '''Test the get_tree() method is FreeDoc'''
        self.assertIs(self.free_doc_root.get_tree(), tree_root)
        self.assertIs(self.free_doc_left.get_tree(), tree_left)
        self.assertIs(self.free_doc_right.get_tree(), tree_right)
        self.assertIs(self.free_doc_leaf.get_tree(), tree_leaf)
        self.assertIs(self.free_doc_recursive.get_tree(), tree_recursive)

    def test_free_doc_eq(self):
        '''Test FreeDoc.__eq__'''
        doc1 = FreeDoc(ET.ElementTree(a))
        doc2 = FreeDoc(ET.ElementTree(d))
        doc3 = FreeDoc(ET.ElementTree(d2))

        self.assertEqual(doc1, doc1)
        self.assertEqual(doc2, doc2)
        self.assertNotEqual(doc2, doc3)
        self.assertEqual(None, None)
        self.assertNotEqual(doc1, doc2)
        self.assertNotEqual(doc1, None)

    # Docs
    def test_docs(self):
        '''Test Docs template constructor'''
        docs = Docs(self.CLASS_DOCS, self.FREE_DOCS)

        self.assertIs(docs.class_docs, self.CLASS_DOCS)
        self.assertIs(docs.free_docs, self.FREE_DOCS)

    def test_get_class_docs(self):
        docs = Docs(self.CLASS_DOCS, self.FREE_DOCS)

        for doc_name in self.CLASS_DOCS.keys():
            self.assertIs(
                self.CLASS_DOCS.get(doc_name), docs.get_class_docs(doc_name))

    def test_get_free_docs(self):
        docs = Docs(self.CLASS_DOCS, self.FREE_DOCS)

        for doc_name in self.FREE_DOCS.keys():
            self.assertIs(
                self.FREE_DOCS.get(doc_name), docs.get_free_docs(doc_name))

    def test_get_class_docs_keys_list(self):
        docs = Docs(self.CLASS_DOCS, self.FREE_DOCS)
        class_doc_keys = list(self.CLASS_DOCS)
        docs_list = docs.get_class_docs_keys_list()

        self.assertEqual(len(self.CLASS_DOCS), len(docs_list))

        for key in class_doc_keys:
            self.assertIn(key, docs_list)

    def test_get_free_docs_keys_list(self):
        docs = Docs(self.CLASS_DOCS, self.FREE_DOCS)
        free_doc_keys = list(self.FREE_DOCS)
        docs_list = docs.get_free_docs_keys_list()

        self.assertEqual(len(self.FREE_DOCS), len(docs_list))

        for key in free_doc_keys:
            self.assertIn(key, docs_list)

    def test_get_class_docs_values_list(self):
        docs = Docs(self.CLASS_DOCS, self.FREE_DOCS)
        docs_list = docs.get_class_docs_values_list()

        self.assertEqual(len(self.CLASS_DOCS), len(docs_list))
        self.assertIn(tree_root, docs_list)
        self.assertIn(tree_left, docs_list)
        self.assertIn(tree_right, docs_list)
        self.assertIn(tree_leaf, docs_list)
        self.assertIn(tree_recursive, docs_list)

    def test_get_free_docs_values_list(self):
        docs = Docs(self.CLASS_DOCS, self.FREE_DOCS)
        docs_list = docs.get_free_docs_values_list()

        self.assertEqual(len(self.FREE_DOCS), len(docs_list))
        self.assertIn(tree_root, docs_list)
        self.assertIn(tree_left, docs_list)
        self.assertIn(tree_right, docs_list)
        self.assertIn(tree_leaf, docs_list)
        self.assertIn(tree_recursive, docs_list)


if __name__ == "__main__":
    unittest.main()
