import io
import unittest
from contextlib import redirect_stdout,redirect_stderr
from tempfile import NamedTemporaryFile
from dependency_planner import plan,CycleError,main

class PlannerTests(unittest.TestCase):
    def test_diamond(self):
        graph={'deploy':['tests','lint'],'tests':['build'],'lint':['build'],'build':[]}
        self.assertEqual(plan(graph),{'waves':[['build'],['lint','tests'],['deploy']],'order':['build','lint','tests','deploy']})
        self.assertEqual(graph['deploy'],['tests','lint'])
    def test_duplicate_and_disconnected(self):
        self.assertEqual(plan({'c':['a','a'],'b':[],'a':[]})['waves'],[['a','b'],['c']])
    def test_cycles_and_blocked(self):
        with self.assertRaises(CycleError) as context: plan({'a':['b'],'b':['a'],'downstream':['a'],'free':[]})
        self.assertEqual(context.exception.blocked,('a','b','downstream'))
        with self.assertRaises(CycleError): plan({'self':['self']})
    def test_invalid(self):
        for graph in [[],{'a':['missing']},{'a':'b'},{'':[]},{'a':[1]}]:
            with self.assertRaises(ValueError): plan(graph)
    def test_empty(self): self.assertEqual(plan({}),{'waves':[],'order':[]})
    def test_cli(self):
        with NamedTemporaryFile(mode='w+',encoding='utf-8') as file:
            file.write('{"build":[],"test":["build"]}'); file.flush()
            with redirect_stdout(io.StringIO()): self.assertEqual(main([file.name]),0)
        with redirect_stderr(io.StringIO()): self.assertEqual(main(['missing-file']),2)
