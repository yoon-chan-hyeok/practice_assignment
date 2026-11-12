"""검수 보조 코드의 단위 테스트. DB의 SQL 실행 테스트가 아닙니다."""
import unittest
from pathlib import Path
from sql_tools import mask_sql, parse_steps, capture_once, replace_runtime_ids
from verify_postgres import compile_level, ROOT

class ToolTests(unittest.TestCase):
    def test_line_comment(self):
        self.assertNotIn('DROP',mask_sql("SELECT 1; -- DROP TABLE\n"))
    def test_nested_comments(self):
        self.assertNotIn('DROP',mask_sql("/* a /* DROP */ x */ SELECT 1;"))
    def test_quoted_semicolon(self):
        self.assertEqual(mask_sql("SELECT 'a;''b';").count(';'),1)
    def test_dollar_block(self):
        self.assertEqual(mask_sql('DO $x$ BEGIN PERFORM 1; END $x$;').count(';'),1)
    def test_unclosed_string(self):
        with self.assertRaises(ValueError):mask_sql("SELECT 'oops")
    def test_unclosed_comment(self):
        with self.assertRaises(ValueError):mask_sql('/* broken')
    def test_capture_not_reexecuted(self):
        out=capture_once("INSERT INTO x(a) VALUES (';') RETURNING id;\n-- end",'a_')
        self.assertIn('\\gset a_',out)
        self.assertNotIn(';',mask_sql(out.split('\\gset')[0]))
        self.assertEqual(out.count('INSERT'),1)
    def test_capture_multiple_statements_rejected(self):
        with self.assertRaises(ValueError):capture_once('SELECT 1; SELECT 2;','x_')
    def test_unfinished_rejected(self):
        with self.assertRaises(ValueError):replace_runtime_ids('SELECT __TODO_COL__;')
    def test_runtime_replaced(self):
        self.assertEqual(replace_runtime_ids('SELECT __A_ID__;'),'SELECT :a_id;')
    def test_comment_todo_allowed(self):
        self.assertIn('SELECT 1;',replace_runtime_ids('-- __TODO_COMMENT__\nSELECT 1;'))
    def test_parse_step(self):
        x=parse_steps('-- @step one expect=23514 capture=- reconnect=false\nSELECT 1;')
        self.assertEqual(x[0].expect,'23514')
    def test_all_level_rendering(self):
        for level in ['B','A','H']:
            with self.subTest(level=level):
                sql,expected=compile_level(level,'knowledge_lab_verify_000000000001',ROOT)
                self.assertIn('@@COMPLETE '+level,sql)
                self.assertEqual(sql.count('\\connect '),3)
                self.assertIn('D8_OLD_PRESERVED',sql)
                self.assertIn('D8_GROUP_TOTAL',sql)
                self.assertEqual(expected['D8_CHECK_FAIL'],'23514')
                self.assertEqual(expected['D8_FK_FAIL'],'23503')
                self.assertNotIn('__TODO_',mask_sql(sql))
    def test_students_are_not_solutions(self):
        student=ROOT.parent/'수강생용'
        if not student.exists():self.skipTest('통합본에서만 수강생 경로 대조')
        with self.assertRaises(ValueError):compile_level('B','knowledge_lab_verify_000000000001',student)

if __name__=='__main__':unittest.main(verbosity=2)
