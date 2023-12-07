import unittest

import src.model.callstack_data as callstack_data


class TestCallGraph(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.call_graph = callstack_data.CallGraph()

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

    def test_parse_single_line(self):
        self.call_graph.clear()
        stack_list = ["main+0"]
        self.call_graph.parse(stack_list)
        self.assertEqual(self.call_graph.nx_graph.nodes["main"]['count'], 1)
        self.assertEqual(self.call_graph.nx_graph.nodes["main"]['traced'], True)

    def test_parse_multiple_lines(self):
        self.call_graph.clear()
        stack_list = ["main+0", "add_number+0", "multiply_number+0"]
        self.call_graph.parse(stack_list)
        self.assertEqual(self.call_graph.nx_graph.nodes["main"]['count'], 1)
        self.assertEqual(self.call_graph.nx_graph.nodes["main"]['traced'], True)
        self.assertEqual(self.call_graph.nx_graph.nodes["add_number"]['count'], 1)
        self.assertEqual(self.call_graph.nx_graph.nodes["add_number"]['traced'], False)
        self.assertEqual(self.call_graph.nx_graph.nodes["multiply_number"]['count'], 1)
        self.assertEqual(self.call_graph.nx_graph.nodes["multiply_number"]['traced'], False)
        self.assertEqual(self.call_graph.nx_graph.edges[("add_number", "main")]['weight'], 1)
        self.assertEqual(self.call_graph.nx_graph.edges[("multiply_number", "add_number")]['weight'], 1)

    def test_parse_multiple_lines_with_repeated_nodes(self):
        self.call_graph.clear()
        stack_list = ["main+0", "add_number+0", "multiply_number+0", "add_number+0"]
        self.call_graph.parse(stack_list)
        self.assertEqual(self.call_graph.nx_graph.nodes["main"]['count'], 1)
        self.assertEqual(self.call_graph.nx_graph.nodes["main"]['traced'], True)
        self.assertEqual(self.call_graph.nx_graph.nodes["add_number"]['count'], 2)
        self.assertEqual(self.call_graph.nx_graph.nodes["add_number"]['traced'], False)
        self.assertEqual(self.call_graph.nx_graph.nodes["multiply_number"]['count'], 1)
        self.assertEqual(self.call_graph.nx_graph.nodes["multiply_number"]['traced'], False)
        self.assertEqual(self.call_graph.nx_graph.edges[("add_number", "main")]['weight'], 1)
        self.assertEqual(self.call_graph.nx_graph.edges[("multiply_number", "add_number")]['weight'], 1)
        self.assertEqual(self.call_graph.nx_graph.edges[("add_number", "multiply_number")]['weight'], 1)

    def test_parse_multiple_lines_with_repeated_nodes_and_different_offset(self):
        self.call_graph.clear()
        stack_list = ["main+4", "add_number+15", "multiply_number+5", "add_number+20"]
        self.call_graph.parse(stack_list)
        self.assertEqual(self.call_graph.nx_graph.nodes["main"]['count'], 1)
        self.assertEqual(self.call_graph.nx_graph.nodes["main"]['traced'], True)
        self.assertEqual(self.call_graph.nx_graph.nodes["add_number"]['count'], 2)
        self.assertEqual(self.call_graph.nx_graph.nodes["add_number"]['traced'], False)
        self.assertEqual(self.call_graph.nx_graph.nodes["multiply_number"]['count'], 1)
        self.assertEqual(self.call_graph.nx_graph.nodes["multiply_number"]['traced'], False)
        self.assertEqual(self.call_graph.nx_graph.edges[("add_number", "main")]['weight'], 1)
        self.assertEqual(self.call_graph.nx_graph.edges[("multiply_number", "add_number")]['weight'], 1)
        self.assertEqual(self.call_graph.nx_graph.edges[("add_number", "multiply_number")]['weight'], 1)

    def test_multiple_parse(self):
        self.call_graph.clear()
        stack_list = ["traced_method", "add_number+0", "multiply_number+0", "add_number+0"]
        stack_list_2 = ["traced_method", "add_number+0", "multiply_number+0", "add_number+0"]
        self.call_graph.parse(stack_list)
        self.call_graph.parse(stack_list_2)
        self.assertEqual(self.call_graph.nx_graph.nodes["traced_method"]['count'], 2)
        self.assertEqual(self.call_graph.nx_graph.nodes["traced_method"]['traced'], True)
        self.assertEqual(self.call_graph.nx_graph.nodes["add_number"]['count'], 4)
        self.assertEqual(self.call_graph.nx_graph.nodes["add_number"]['traced'], False)
        self.assertEqual(self.call_graph.nx_graph.nodes["multiply_number"]['count'], 2)
        self.assertEqual(self.call_graph.nx_graph.nodes["multiply_number"]['traced'], False)
        self.assertEqual(self.call_graph.nx_graph.edges[("add_number", "traced_method")]['weight'], 2)
        self.assertEqual(self.call_graph.nx_graph.edges[("multiply_number", "add_number")]['weight'], 2)
        self.assertEqual(self.call_graph.nx_graph.edges[("add_number", "multiply_number")]['weight'], 2)

    def test_multiple_parse_different_route(self):
        self.call_graph.clear()
        stack_list = ["traced_method", "add_number+0", "multiply_number+0", "add_number+0"]
        stack_list_2 = ["traced_method", "add_number+0", "print_number+30", "decrease_number+4"]
        self.call_graph.parse(stack_list)
        self.call_graph.parse(stack_list_2)
        self.assertEqual(self.call_graph.nx_graph.nodes["traced_method"]['count'], 2)
        self.assertEqual(self.call_graph.nx_graph.nodes["traced_method"]['traced'], True)
        self.assertEqual(self.call_graph.nx_graph.nodes["add_number"]['count'], 3)
        self.assertEqual(self.call_graph.nx_graph.nodes["add_number"]['traced'], False)
        self.assertEqual(self.call_graph.nx_graph.nodes["multiply_number"]['count'], 1)
        self.assertEqual(self.call_graph.nx_graph.nodes["multiply_number"]['traced'], False)
        self.assertEqual(self.call_graph.nx_graph.nodes["print_number"]['count'], 1)
        self.assertEqual(self.call_graph.nx_graph.nodes["print_number"]['traced'], False)
        self.assertEqual(self.call_graph.nx_graph.nodes["decrease_number"]['count'], 1)
        self.assertEqual(self.call_graph.nx_graph.nodes["decrease_number"]['traced'], False)
        self.assertEqual(self.call_graph.nx_graph.edges[("add_number", "traced_method")]['weight'], 2)
        self.assertEqual(self.call_graph.nx_graph.edges[("multiply_number", "add_number")]['weight'], 1)
        self.assertEqual(self.call_graph.nx_graph.edges[("add_number", "multiply_number")]['weight'], 1)
        self.assertEqual(self.call_graph.nx_graph.edges[("print_number", "add_number")]['weight'], 1)
        self.assertEqual(self.call_graph.nx_graph.edges[("decrease_number", "print_number")]['weight'], 1)

    def test_clear(self):
        self.call_graph.clear()
        stack_list = ["traced_method", "add_number+0", "multiply_number+0", "add_number+0"]
        self.call_graph.parse(stack_list)
        self.call_graph.clear()
        self.assertEqual(len(self.call_graph.nx_graph.nodes), 0)
        self.assertEqual(len(self.call_graph.nx_graph.edges), 0)


if __name__ == '__main__':
    unittest.main()
