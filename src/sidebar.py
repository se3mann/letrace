from gi.repository import Gtk
from trace_utils import TraceUtils, Str

@Gtk.Template(filename="sidebar.ui")
class TraceSideBar(Gtk.Box):
    __gtype_name__ = 'TraceSideBar'

    search_entry = Gtk.Template.Child()
    sidebar_switcher = Gtk.Template.Child()
    sidebar_stack = Gtk.Template.Child()
    methods_from_file = Gtk.Template.Child()
    methods_from_kernel = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_entry.connect("search-changed", self.on_search_changed)
        self.setup_singleselect_listview(TraceUtils.test_list)
        print("Sidebar init")
        TraceUtils.test_list.append(Str("test1"))
        TraceUtils.test_list.append(Str("test2"))
        TraceUtils.test_list.append(Str("test3"))
        for i in range(50):
            TraceUtils.test_list.append(Str(f"test{i}"))
        print(TraceUtils.test_list.get_n_items())


    def get_active_stack(self):
        return self.sidebar_stack.get_visible_child_name()

    def on_search_changed(self, entry):
        pass

    def setup_singleselect_listview(self, data):
        singleselect = Gtk.SingleSelection()
        singleselect.set_model(data)
        # factory for ListView widget
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", lambda _fact, item:
            item.set_child(Gtk.Label(halign=Gtk.Align.START))
        )
        factory.connect("bind", lambda _fact, item:
            item.get_child().set_label(item.get_item()._value)
        )

        self.methods_from_kernel.set_model(singleselect)
        self.methods_from_kernel.set_factory(factory)