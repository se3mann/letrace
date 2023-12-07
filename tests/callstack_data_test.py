import unittest

import src.model.callstack_data as callstack_data

class TestCallGraph(unittest.TestCase):
    def test_delete_offset_offset(self):
        method_width_offset_1 = "add_number+30"
        method_width_offset_2 = "add_number+0"
        method_width_offset_3 = "add_number+1234567"

        result_1 = callstack_data.delete_offset(method_width_offset_1)
        result_2 = callstack_data.delete_offset(method_width_offset_2)
        result_3 = callstack_data.delete_offset(method_width_offset_3)

        self.assertEqual(result_1, "add_number")
        self.assertEqual(result_2, "add_number")
        self.assertEqual(result_3, "add_number")

    def test_delete_offset_no_offset(self):
        method_1 = "main"
        method_2 = "multiply_number"
        method_3 = "__init__"

        result_1 = callstack_data.delete_offset(method_1)
        result_2 = callstack_data.delete_offset(method_2)
        result_3 = callstack_data.delete_offset(method_3)

        self.assertEqual(result_1, "main")
        self.assertEqual(result_2, "multiply_number")
        self.assertEqual(result_3, "__init__")

if __name__ == '__main__':
    unittest.main()

